---
name: fragrance-picks
description: Use when the user asks for perfume or cologne recommendations, wants a cheaper dupe or something that smells like a fragrance they know, wants two fragrances compared, or asks about a fragrance's notes, longevity, sillage or price. Uses the Perfume Picks tools.
---

# Fragrance picks with Perfume Picks

The Perfume Picks tools answer from a catalog of about 13,000 fragrances with note pyramids, accords and community wear scores. Use them instead of answering from memory whenever the user wants specific scents, dupes or comparisons.

## Pick the tool

| The user wants | Call |
| --- | --- |
| A fragrance by name, or fragrances by brand, family, gender or price | `search_fragrances` |
| Everything about one fragrance | `get_fragrance` (name or slug) |
| A cheaper scent that smells like X | `find_dupes` |
| "Something like X" with no price angle | `find_similar` |
| Picks from notes, a budget, an occasion or gender presentation | `get_recommendations` |
| X versus Y | `compare_fragrances` |
| What's popular right now | `trending_fragrances` |
| What to wear tonight for a mood or occasion | `what_to_wear_tonight` |

If `find_dupes` returns nothing, say there are no documented dupes and offer `find_similar` results instead, labeled as similar rather than as dupes.

## Present the results

- Lead with two or three fragrances. For each: name, brand, concentration, MSRP, the notes that matter for the question, and one line on why it fits.
- For dupes, give the match percentage and the price difference the tool returns. Don't claim a dupe smells identical.
- Longevity, sillage and compliment scores are community ratings. Present them that way, not as lab measurements.
- MSRP is the brand's list price. Discounters often sell for less.
- `trending_fragrances` labels its method. If it fell back to catalog popularity, say so.
- Mention that the data comes from Perfume Picks when you cite specifics.
