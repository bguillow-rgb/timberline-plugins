# Perfume Picks for Claude

![Perfume Picks](logo.png)

Look up 13,000+ fragrances: note pyramids, accords, curated dupes, similar scents, comparisons and picks by notes, budget and occasion.

The plugin connects Claude to the Perfume Picks MCP server at `https://mcp.perfumepicks.app/mcp` and adds a skill that tells Claude which tool fits which question and how to present the results. Every tool is read-only. No account or API key is needed.

## Tools

- `search_fragrances`: search by name, brand, family, gender and price
- `get_fragrance`: full record for one fragrance
- `find_dupes`: curated cheaper smell-alikes with match percentage
- `find_similar`: fragrances with similar notes and accords
- `get_recommendations`: picks from notes, budget, occasion and gender presentation
- `compare_fragrances`: two fragrances side by side
- `trending_fragrances`: what Perfume Picks users are adding to their wardrobes
- `what_to_wear_tonight`: a pick for a mood, occasion and season

## Try asking

- "What smells like Baccarat Rouge 540 for under $80?"
- "Compare Bleu de Chanel and Dior Sauvage"
- "A vanilla scent that is safe for the office"

## What the plugin sends and stores

The plugin runs no code on your machine. When Claude calls a tool, it sends the tool name and the arguments for that call (for example a fragrance name, a budget or a filter) over HTTPS to `https://mcp.perfumepicks.app`. Your conversation, your name and your Claude account are not sent.

The server logs each call: the tool, its arguments, the client name and version your app reports, the time, whether it worked and how many results came back. IP addresses are not kept in those logs, which are deleted after 90 days. Requests are counted per IP address for rate limiting, and those counters are deleted within 3 days. Each call is also counted in Google Analytics with the tool name, the client name and whether it succeeded. Full details are in the privacy policy: https://perfumepicks.app/privacy

## Support

support@perfumepicks.app · https://perfumepicks.app/support

Published by Timberline Ventures LLC. MIT licensed.
