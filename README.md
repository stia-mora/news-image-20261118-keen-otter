# THE WORLD IN ONE DAY — news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/stia-mora/news-image-20261118-keen-otter/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/stia-mora/news-image-20261118-keen-otter/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page summarising the world news of
**Wednesday, 18 November 2026** in a single image: six stories, six regions,
one day.

## The six stories

| Region | Story |
| --- | --- |
| ASIA | APEC summit opens in Shenzhen; Xi–Trump–Putin trilateral set for 19 Nov |
| ASIA | Quad leaders meet in Manila, unveil new plan |
| ASIA | North Korea fires ballistic missile toward Sea of Japan |
| MIDDLE EAST | Iran claims drone strike on US radar site in Bahrain |
| BUSINESS | US stocks plunge as Dow drops 1,000 points intraday |
| WEATHER | Cyclone Akvan strengthens over Bay of Bengal |

Wording follows the reporting (Reuters, AP, White House, IMD) and hedges
where the record is uncertain — "said", "claimed", "reported" — rather than
stating speculation as fact.

## How it was made

No AI-generated imagery. `draw.py` renders everything with PIL:
cream paper, navy type, one red accent, and six flat geometric icons
(skyline, plane, missile, drone, falling chart, cyclone spiral) drawn from
lines, arcs and polygons. All text is real rendered type (DejaVu Sans),
checked by eye at full size for clarity, overflow and overlap.

## Run it

```sh
# Regenerate the image (needs Pillow)
python3 draw.py          # writes entry.png (1024x1024, <= 1 MiB)

# Copy it to the output directory (Node 22, standard library only)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the `entry.png` beside it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), byte for byte —
two runs produce identical output.
