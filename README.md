# Timberline plugins for Claude

Read-only Claude plugins from Timberline Ventures LLC. Each one connects Claude to a public catalog through an MCP server and adds a skill that tells Claude which tool fits which question.

| Plugin | What it looks up | MCP server |
| --- | --- | --- |
| [Pour Picks](pour-picks/) | 4,700+ bourbons, ryes, scotches and other spirits | `https://mcp.pourpicks.app/mcp` |
| [Perfume Picks](perfume-picks/) | 13,000+ fragrances and curated dupes | `https://mcp.perfumepicks.app/mcp` |
| [Percolate](percolate/) | 1,100+ specialty coffees and brew recipes | `https://mcp.percolateapp.com/mcp` |
| [ITIN Finance](itin-finance/) | Loans, credit and banking for ITIN holders, in English and Spanish | `https://mcp.itinlending.net/mcp` |

None of them need an account or an API key, and none run code on your machine. Each plugin's README says exactly what is sent and stored.

## Install in Claude Code

```
/plugin marketplace add bguillow-rgb/timberline-plugins
/plugin install pour-picks@timberline
```

Swap in `perfume-picks`, `percolate` or `itin-finance` for the others.

## Use the server alone in Claude or another MCP client

Add the server URL from the table above as a custom connector. You get the tools without the skill.

MIT licensed. Questions: info@timberlineventuresllc.com
