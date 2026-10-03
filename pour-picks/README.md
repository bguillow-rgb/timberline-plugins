# Pour Picks for Claude

![Pour Picks](logo.png)

Look up 4,700+ bourbons, ryes, scotches and other spirits: tasting profiles, similar bottles, cheaper alternatives, comparisons and picks by flavor and budget.

The plugin connects Claude to the Pour Picks MCP server at `https://mcp.pourpicks.app/mcp` and adds a skill that tells Claude which tool fits which question and how to present the results. Every tool is read-only. No account or API key is needed.

## Tools

- `search_bottles`: search the catalog by name, category, price and proof
- `get_bottle`: full record for one bottle
- `find_similar`: bottles with a similar flavor profile
- `find_cheaper_alternative`: similar bottles that cost less
- `get_recommendations`: picks from flavor keywords, budget and occasion
- `compare_bottles`: two bottles side by side
- `trending_bottles`: what Pour Picks users are adding to their cellars
- `pour_tonight_suggestion`: a pick for a mood, occasion and season

## Try asking

- "Something like Eagle Rare but cheaper"
- "Compare Buffalo Trace and Weller Special Reserve"
- "A smoky scotch around $60 for a gift"

## What the plugin sends and stores

The plugin runs no code on your machine. When Claude calls a tool, it sends the tool name and the arguments for that call (for example a bottle name, a budget or a filter) over HTTPS to `https://mcp.pourpicks.app`. Your conversation, your name and your Claude account are not sent.

The server logs each call: the tool, its arguments, the client name and version your app reports, the time, whether it worked and how many results came back. IP addresses are not kept in those logs, which are deleted after 90 days. Requests are counted per IP address for rate limiting, and those counters are deleted within 3 days. Each call is also counted in Google Analytics with the tool name, the client name and whether it succeeded. Full details are in the privacy policy: https://pourpicks.app/privacy

## Support

support@pourpicks.app · https://pourpicks.app/support

Published by Timberline Ventures LLC. MIT licensed.
