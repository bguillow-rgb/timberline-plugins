---
name: itin-finance-answers
description: Use when the user asks about loans, mortgages, credit cards, credit scores or banking for someone with an ITIN instead of a Social Security number, which institutions accept ITIN applicants, or how to get an ITIN. Works in English and Spanish. Uses the ITIN finance tools.
---

# ITIN finance answers

The ITIN finance tools answer from a network of editorial guides and a directory of institutions that accept ITIN applicants. Each institution entry says whether it was verified against the institution's own pages, with citation URLs and dates. Use the tools whenever the user needs specific institutions, requirements or steps.

## Pick the tool

| The user wants | Call |
| --- | --- |
| "Can I get a [loan or card] with an ITIN?" | `can_i_get_this_loan` (add their state if they gave one) |
| Institutions that accept ITIN for a loan or card type, optionally in a state | `find_itin_lenders` |
| Details on one institution | `get_lender_details` |
| A specific factual question | `faq_lookup` |
| A topic overview or a guide | `search_guides`, then `get_guide` |
| State rules (driver's licenses, taxes paid) | `itin_state_info` |
| How to apply for an ITIN | `how_to_get_an_itin` |

Pass `lang: "es"` when the user writes in Spanish, and answer in Spanish.

## Accuracy rules

- Report each institution's verification status as the tool gives it. If an entry is unverified, say so, and tell the user to confirm with the institution before applying.
- Give the citation URL and its date when you state a requirement, rate or down payment. Terms change.
- Don't promise approval or estimate the user's odds. Requirements are what the institution publishes. Approval depends on the application.
- This is general information, not financial or legal advice. For immigration-status questions beyond what the guides cover, suggest an immigration attorney or a DOJ-accredited representative.
- Link the guide URLs the tools return so the user can read the full article.
