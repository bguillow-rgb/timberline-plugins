# ITIN Finance for Claude

![ITIN Finance](logo.png)

Answers for people with an ITIN instead of an SSN: loans, mortgages, credit cards and credit scores, plus a verified directory of institutions that accept ITIN applicants. English and Spanish.

The plugin connects Claude to the ITIN Finance MCP server at `https://mcp.itinlending.net/mcp` and adds a skill that tells Claude which tool fits which question and how to present the results. Every tool is read-only. No account or API key is needed.

## Tools

- `search_guides`: search 290+ guides in English and Spanish
- `get_guide`: one guide with its quick answer and FAQs
- `faq_lookup`: a direct answer from 1,800+ FAQs
- `find_itin_lenders`: institutions that accept ITIN applicants, by loan type and state
- `get_lender_details`: one institution, with citations and verification dates
- `can_i_get_this_loan`: can I get this loan type with an ITIN?
- `itin_state_info`: state facts for ITIN holders
- `how_to_get_an_itin`: how to apply for an ITIN with Form W-7

## Try asking

- "Can I get a mortgage in Texas with an ITIN?"
- "¿Qué tarjetas de crédito aceptan ITIN?"
- "Which credit unions in California give car loans to ITIN holders?"

## What the plugin sends and stores

The plugin runs no code on your machine. When Claude calls a tool, it sends the tool name and the arguments for that call (for example a guide name, a budget or a filter) over HTTPS to `https://mcp.itinlending.net`. Your conversation, your name and your Claude account are not sent.

The server logs each call: the tool, its arguments, the client name and version your app reports, the time, whether it worked and how many results came back. IP addresses are not kept in those logs, which are deleted after 90 days. Requests are counted per IP address for rate limiting, and those counters are deleted within 3 days. Each call is also counted in Google Analytics with the tool name, the client name and whether it succeeded. Full details are in the privacy policy: https://itinlending.net/privacy

## Support

info@timberlineventuresllc.com · https://itinlending.net/contact

Published by Timberline Ventures LLC. MIT licensed.
