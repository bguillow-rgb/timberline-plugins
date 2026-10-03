# Percolate for Claude

![Percolate](logo.png)

Look up 1,100+ specialty coffees: tasting profiles, similar coffees, comparisons, brew recipes and picks by flavor, roast, budget and brew gear.

The plugin connects Claude to the Percolate MCP server at `https://mcp.percolateapp.com/mcp` and adds a skill that tells Claude which tool fits which question and how to present the results. Every tool is read-only. No account or API key is needed.

## Tools

- `search_coffees`: search by category, roast, brew method and price
- `get_coffee`: full record for one coffee
- `find_similar`: coffees with a similar profile
- `get_recommendations`: picks from flavors, budget, roast and the gear you own
- `compare_coffees`: two coffees side by side
- `trending_coffees`: what Percolate users are adding to their collections
- `dial_in_suggestion`: ratio, temperature and grind for a coffee
- `what_to_brew`: a pick for the time of day, mood and brew method

## Try asking

- "A chocolatey espresso blend under $20"
- "How should I dial in Stumptown Hair Bender on a V60?"
- "Something like Stumptown Hair Bender but a lighter roast"

## What the plugin sends and stores

The plugin runs no code on your machine. When Claude calls a tool, it sends the tool name and the arguments for that call (for example a coffee name, a budget or a filter) over HTTPS to `https://mcp.percolateapp.com`. Your conversation, your name and your Claude account are not sent.

The server logs each call: the tool, its arguments, the client name and version your app reports, the time, whether it worked and how many results came back. IP addresses are not kept in those logs, which are deleted after 90 days. Requests are counted per IP address for rate limiting, and those counters are deleted within 3 days. Each call is also counted in Google Analytics with the tool name, the client name and whether it succeeded. Full details are in the privacy policy: https://percolateapp.com/privacy

## Support

support@percolateapp.com · https://percolateapp.com/support

Published by Timberline Ventures LLC. MIT licensed.
