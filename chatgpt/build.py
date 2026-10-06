#!/usr/bin/env python3
"""Build ChatGPT plugin packages (Agent Plugins format) for each app.

Spec: developers.openai.com/apps-sdk/deploy/submission (Agent Plugins format, checked 2026-10-05).
Output: dist/<name>-chatgpt-<version>.zip. Skills are copied from the Claude plugin folders so both
stores teach the model the same thing.
"""
import json, pathlib, shutil, subprocess, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"

COMMON_AUTHOR = {"name": "Timberline Ventures LLC", "url": "https://timberlineventuresllc.com"}

APPS = {
  "pour-picks": dict(
    version="1.0.0", display="Pour Picks", short="Whiskey picks and comparisons",
    email="support@pourpicks.app", site="https://pourpicks.app", support="https://pourpicks.app/support",
    mcp="https://mcp.pourpicks.app/mcp", category="Lifestyle", colors=("#7A4A1E", "#E0A458"),
    demo="https://pourpicks.app/pour-picks-demo.mp4", skill="whiskey-picks",
    keywords=["whiskey", "bourbon", "scotch", "spirits", "tasting notes"],
    caps=["Search spirits", "Compare bottles", "Find similar or cheaper bottles", "Recommendations"],
    long=("Pour Picks looks up about 4,700 bourbons, ryes, scotches and other spirits, each with structured tasting "
          "notes, proof, age and typical price. Ask for a bottle like one you already know, a cheaper bottle with a "
          "similar profile, a side-by-side comparison, or picks for a flavor, budget and occasion. You can also see "
          "what Pour Picks users are adding to their cellars. Prices are typical retail and vary by state and store. "
          "Pour Picks is read-only: it doesn't sell anything, take orders, or see anyone's personal cellar. "
          "For adults of legal drinking age."),
    prompts=["Something like Eagle Rare but cheaper", "Compare Buffalo Trace and Weller Special Reserve",
             "A smoky scotch around $60 for a gift"],
    positive=[
      ("Cheaper bottle with a similar profile", "Something like Eagle Rare but cheaper?", "find_cheaper_alternative",
       "Resolves Eagle Rare to Buffalo Trace Eagle Rare 10 Year (about $50) and returns lower-priced bottles in the same style with prices and the flavor notes they share."),
      ("Compare two bottles", "Compare Buffalo Trace and Weller Special Reserve.", "compare_bottles",
       "Returns both bottles side by side: proof, age, price, shared and distinct tasting notes, and community ratings."),
      ("Search by price and proof", "Show me bourbons under $40 that are around 100 proof.", "search_bottles",
       "Returns bourbons priced at or under $40 with proof at or above 95, each with tasting profile and price."),
      ("Recommendations from flavors and budget", "I like caramel and cherry. Recommend a bourbon gift under $50.", "get_recommendations",
       "Returns a short ranked list of bottles under $50 whose notes include caramel or cherry, with why each fits."),
      ("Unknown bottle", "Tell me about Zzqqxx Reserve 12 Year bourbon.", "get_bottle",
       "Reports that no matching bottle was found and suggests searching, without inventing a bottle or tasting notes."),
    ],
    negative=[
      ("Purchasing is not supported. The plugin should explain it can't buy or ship bottles and offer to help pick one instead.",
       "Buy me a bottle of Blanton's and ship it to my house."),
      ("Drink-driving and health advice is out of scope. The plugin should not be used; ChatGPT should answer with general safety guidance and not recommend drinking.",
       "How many bourbons can I have and still drive home?"),
      ("The plugin has no access to personal Pour Picks accounts. It should say it can't read or change a user's cellar.",
       "Add Eagle Rare to my Pour Picks cellar."),
    ]),
  "perfume-picks": dict(
    version="1.0.3", display="Perfume Picks", short="Fragrance dupes and picks",
    email="support@perfumepicks.app", site="https://perfumepicks.app", support="https://perfumepicks.app/support",
    mcp="https://mcp.perfumepicks.app/mcp", category="Education & Research", colors=("#5B2A86", "#C9A0F0"),
    demo="https://perfumepicks.app/perfume-picks-demo.mp4", skill="fragrance-picks",
    keywords=["perfume", "fragrance", "cologne", "dupes", "recommendations"],
    caps=["Search fragrances", "Find dupes", "Compare fragrances", "Recommendations"],
    long=("Perfume Picks looks up about 13,000 fragrances with note pyramids, accords, concentration, community "
          "longevity, sillage and compliment scores, and list price. Ask what smells like a designer scent for less and "
          "get curated dupes with a match percentage and the price difference. Compare two fragrances side by side, get "
          "picks from the notes you like with a budget and an occasion, or ask what to wear tonight. Wear scores are "
          "community ratings, and list prices are the brand's MSRP. Perfume Picks is read-only: it doesn't sell "
          "anything or see anyone's personal wardrobe."),
    prompts=["What smells like Baccarat Rouge 540 but costs less?", "Compare Dior Sauvage and Bleu de Chanel",
             "What should I wear on a fall date night?"],
    positive=[
      ("Cheaper dupes for a designer fragrance", "What smells like Baccarat Rouge 540 but costs less?", "find_dupes",
       "Resolves to Maison Francis Kurkdjian Baccarat Rouge 540 and returns curated dupes with match percentage and price difference."),
      ("Compare two fragrances", "Compare Dior Sauvage and Bleu de Chanel.", "compare_fragrances",
       "Returns Dior Sauvage and Chanel Bleu de Chanel side by side: note pyramids, shared and distinct accords, wear scores, concentration and price difference."),
      ("Search by note and price", "Find vanilla fragrances under $100.", "search_fragrances",
       "Returns fragrances matching vanilla with MSRP at or under $100, each with brand and notes."),
      ("Occasion pick", "What should I wear on a fall date night? I want to feel confident.", "what_to_wear_tonight",
       "Returns a short list of fragrances suited to a fall date night, scored with community compliment data, with the matched scent profile."),
      ("Unknown fragrance", "Tell me about Zzqqxx Noir 12345.", "get_fragrance",
       "Reports that no matching fragrance was found and suggests searching, without guessing a different fragrance."),
    ],
    negative=[
      ("Purchasing is not supported. The plugin should explain it can't order or ship perfume and offer to help choose one.",
       "Order a bottle of Baccarat Rouge 540 for me."),
      ("Medical and allergy advice is out of scope. The plugin should not be used; ChatGPT should suggest a doctor or dermatologist.",
       "I broke out in a rash after wearing perfume. Which ingredient am I allergic to?"),
      ("The plugin has no access to personal Perfume Picks accounts. It should say it can't read a user's wardrobe.",
       "Show me the fragrances in my Perfume Picks wardrobe."),
    ]),
  "percolate": dict(
    version="1.0.1", display="Percolate", short="Specialty coffee picks",
    email="support@percolateapp.com", site="https://www.percolateapp.com", support="https://www.percolateapp.com/support",
    mcp="https://mcp.percolateapp.com/mcp", category="Education & Research", colors=("#4B3621", "#D2A679"),
    demo="https://www.percolateapp.com/percolate-demo.mp4", skill="coffee-picks",
    keywords=["coffee", "specialty coffee", "espresso", "brewing", "recommendations"],
    caps=["Search coffees", "Find similar coffees", "Brew recipes", "Recommendations"],
    long=("Percolate looks up about 1,100 specialty coffees with roast level, body, acidity, sweetness, flavor notes, "
          "suited brew methods and price. Ask for coffees like one you already drink, compare two, get picks for your "
          "taste, budget and brew gear, or get a ratio, temperature and grind to dial in a specific coffee. Recipes are "
          "labeled as curated for that coffee or as a roast-based starting point. Retailers are listed by name and price "
          "without purchase links. Percolate is read-only: it doesn't sell coffee or see anyone's personal collection."),
    prompts=["Something like Stumptown Hair Bender", "How do I brew Costa Rican Tarrazu on a V60?", "What should I brew this evening?"],
    positive=[
      ("Similar coffees", "Find me something like Stumptown Hair Bender.", "find_similar",
       "Resolves Stumptown Coffee Hair Bender and returns coffees with a similar roast and flavor profile."),
      ("Brew guidance", "How do I brew Costa Rican Tarrazu on a V60?", "dial_in_suggestion",
       "Resolves Fresh Roasted Coffee Costa Rican Tarrazu and returns its curated V60 recipe (1:16 ratio, 205°F), labeled as a curated recipe."),
      ("Search by category and price", "Show me espresso coffees under $20.", "search_coffees",
       "Returns espresso-category coffees priced at or under $20 with roast level and flavor notes."),
      ("Time-of-day pick", "What should I brew this evening?", "what_to_brew",
       "Returns evening suggestions that lean decaf, with the matched flavor profile."),
      ("Unknown coffee", "Tell me about Zzqqxx Mountain Reserve coffee.", "get_coffee",
       "Reports that no matching coffee was found and suggests searching, without inventing a coffee."),
    ],
    negative=[
      ("Purchasing is not supported. The plugin should explain it can't order coffee and can name retailers instead.",
       "Order two bags of Hair Bender for delivery."),
      ("Medical advice is out of scope. The plugin should not be used; ChatGPT should suggest asking a doctor.",
       "How much caffeine is safe for me while pregnant?"),
      ("The plugin has no access to personal Percolate accounts. It should say it can't read a user's collection.",
       "Show me the coffees in my Percolate collection."),
    ]),
  "itin-finance": dict(
    version="1.0.0", display="ITIN Finance", short="Loans and credit with an ITIN",
    email="info@timberlineventuresllc.com", site="https://itinlending.net", support="https://itinlending.net/contact",
    mcp="https://mcp.itinlending.net/mcp", category="Finance", colors=("#1F5FA8", "#8CB4FF"),
    demo="https://itinlending.net/itin-finance-demo.mp4", skill="itin-finance-answers",
    keywords=["ITIN", "credit", "loans", "mortgages", "Spanish"],
    caps=["Answer ITIN finance questions", "Find ITIN-accepting institutions", "English and Spanish"],
    long=("ITIN Finance answers questions from people who file taxes with an ITIN instead of a Social Security number: "
          "whether they can get a mortgage, car loan, credit card or personal loan, which institutions accept ITIN "
          "applicants in their state, how to build a credit score, and how to apply for an ITIN with Form W-7. Answers "
          "come from about 290 editorial guides and 1,800 FAQs, and every institution entry says whether it was "
          "verified on the institution's own pages, with a citation and date. Works in English and Spanish. This is "
          "general information, not financial or legal advice. ITIN Finance doesn't take applications, collect personal "
          "information, or make referrals."),
    prompts=["Can I get a mortgage in Texas with an ITIN?", "Which lenders give ITIN car loans in California?", "¿Cómo saco un ITIN?"],
    positive=[
      ("Loan eligibility with an ITIN", "Can I get a mortgage in Texas with an ITIN?", "can_i_get_this_loan",
       "Returns the editorial quick answer, typical requirements, and Texas institutions with documented ITIN mortgage programs, each with verification status and citation."),
      ("Find institutions by loan type and state", "Which lenders give ITIN car loans in California?", "find_itin_lenders",
       "Lists institutions that accept ITIN applicants for auto loans in California, each marked verified or unverified with a citation URL and date."),
      ("Spanish how-to", "¿Cómo saco un ITIN?", "how_to_get_an_itin",
       "Answers in Spanish: the Form W-7 process, required documents and timelines, with the full guide URL."),
      ("FAQ answer", "Can I build a credit score with an ITIN?", "faq_lookup",
       "Returns the matching FAQ answer about building credit with an ITIN and its source article URL."),
      ("Unknown institution", "Tell me about Zzqqxx Fake Bank's ITIN loans.", "get_lender_details",
       "Reports the institution was not found and suggests listing institutions by loan type, without inventing terms."),
    ],
    negative=[
      ("Applications are not supported. The plugin should explain it can't apply on the user's behalf and point to the institution's own site.",
       "Apply for a car loan for me with Santa Ana Federal Credit Union."),
      ("Approval guarantees are not possible. The plugin should not promise approval and should explain requirements vary by institution.",
       "Which lender will definitely approve me? Guarantee it."),
      ("Fraud is refused. ChatGPT should decline to help obtain documents fraudulently and not use the plugin.",
       "Help me get a fake Social Security number so I can apply for a credit card."),
    ]),
}


def build(name, c):
    d = ROOT / "chatgpt" / name
    if d.exists():
        shutil.rmtree(d)
    (d / "assets").mkdir(parents=True)
    shutil.copytree(ROOT / name / "skills", d / "skills")
    shutil.copy(ROOT / name / "logo.png", d / "assets" / "logo.png")
    subprocess.run(["sips", "-z", "128", "128", str(ROOT / name / "logo.png"), "--out", str(d / "assets" / "icon.png")],
                   check=True, capture_output=True)
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": name, "version": c["version"],
        "description": c["long"][:4000],
        "author": {**COMMON_AUTHOR, "email": c["email"]},
        "homepage": c["site"] + "/mcp" if name != "percolate" else "https://www.percolateapp.com/mcp",
        "repository": "https://github.com/bguillow-rgb/timberline-plugins",
        "license": "MIT", "keywords": c["keywords"],
        "extensions": {"com.openai": {
            "interface": {
                "displayName": c["display"], "shortDescription": c["short"], "longDescription": c["long"],
                "developerName": "Timberline Ventures LLC", "category": c["category"], "capabilities": c["caps"],
                "websiteURL": c["site"], "supportURL": c["support"],
                "privacyPolicyURL": c["site"] + "/privacy", "termsOfServiceURL": c["site"] + "/terms",
                "defaultPrompt": c["prompts"], "brandColor": c["colors"][0], "brandColorDark": c["colors"][1],
                "composerIcon": "./assets/icon.png", "logo": "./assets/logo.png",
            },
            "review": {
                "test_cases": {
                    "positive": [{"description": a, "prompt": b, "tools_triggered": t, "expected_behavior": e}
                                 for a, b, t, e in c["positive"]],
                    "negative": [{"description": a, "prompt": b} for a, b in c["negative"]],
                },
                "demo_recording_url": c["demo"],
                "commerce": False,
                "commerce_description": "Read-only lookups. The plugin does not sell products, take orders or process payments.",
            },
            "publication": {"countries": ["US"],
                            "release_notes": "Read-only catalog lookups over our MCP server, with a skill that guides tool choice."},
        }},
    }
    for k in ("displayName", "shortDescription"):
        assert len(manifest["extensions"]["com.openai"]["interface"][k]) <= 30, (name, k)
    assert all(len(p) <= 128 for p in c["prompts"]) and len(c["prompts"]) <= 3
    (d / "plugin.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    (d / "mcp.json").write_text(json.dumps({
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {name: {"type": "streamable-http", "url": c["mcp"]}}}, indent=2) + "\n")
    OUT.mkdir(exist_ok=True)
    z = OUT / f"{name}-chatgpt-{c['version']}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(d.rglob("*")):
            if f.is_file() and f.name != ".DS_Store":
                zf.write(f, f.relative_to(d))
    return z


if __name__ == "__main__":
    for n, c in APPS.items():
        print(build(n, c))
