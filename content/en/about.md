---
title: "About — Bergen vs Paris"
template: about
---

[← Back to the site](./)

# Bergen vs Paris Weather Comparison

This project compares 10 years of daily weather data (2016–2025) between Bergen, Norway and Paris, France.

- Bergen is on average 5°C colder than Paris, but the gap shrinks to ~4°C in winter
- Daily temperatures are 81% correlated — when one city gets colder, so does the other
- Bergen's snow days average 1.5°C — almost eight in ten are above freezing
- Bergen is geographically closer to the French Riviera than to Arctic Norway
- When Paris bakes above 30°C (114 days over the decade), Bergen averages a comfortable 18°C

## Explore the data

{% data-table /%}

## The process

This project follows the [School of Data pipeline](https://civicliteraci.es/data-pipeline/) methodology: Define, Find, Get, Verify, Clean, Analyse, Present.

### Define

Started with a personal intuition: "Bergen and Paris weather are similar." We broke this into four testable hypotheses:

1. **H1**: Daily mean temperatures are within 3°C of each other
2. **H2**: Temperature changes correlate — when one city cools, so does the other
3. **H3**: Snow events co-occur more than chance would predict
4. **H4**: Sunny days co-occur more than chance would predict

### Find

{% step-meta items="Method: desk research, Sources compared: 6" /%}

Surveyed six data sources (Open-Meteo, Meteostat, Frost API, Météo-France, Visual Crossing, NOAA GSOD). Open-Meteo was the only one with all six required variables (temp mean/min/max, precipitation, snowfall, sunshine) for both cities at 100% completeness, with no API key needed.

### Get

{% step-meta items="Tool: Python (fetch_data.py), API: Open-Meteo" /%}

Fetched 3,653 days of daily data per city from the [Open-Meteo Historical Weather API](https://open-meteo.com/) (ERA5/ECMWF IFS reanalysis). Zero gaps, zero nulls.

### Verify

{% step-meta items="Tool: Python (verify_data.py), Cross-check: ERA5 vs ECMWF IFS models" /%}

- **Completeness**: continuous date sequences, no missing values
- **Quality**: no temperatures outside plausible climate records, no negative precipitation, no suspicious flat-line periods
- **Cross-check**: compared ERA5 vs ECMWF IFS models. Paris data agrees within 1°C on 94% of days. Bergen shows ~1.6°C model uncertainty — noted but not disqualifying

### Clean

{% step-meta items="Tool: Python (clean_data.py), Output: data/clean/horizon.csv" /%}

Merged both cities into a single horizon table (13 columns, daily granularity). Standardised units (sunshine to hours, snowfall to mm). Initially flagged extreme days (Paris max >35°C, Bergen min <−10°C) but a sensitivity check showed removing them changed results by <0.5°C, so we dropped the filtering.

### Analyse

{% step-meta items="Tool: Python (analyse.py), Methods: descriptive statistics, Pearson correlation, co-occurrence analysis" /%}

The analysis tested each hypothesis using simple statistical methods: daily temperature differences and their distributions (H1), Pearson correlation with lag analysis (H2), and co-occurrence rates compared to chance baselines (H3, H4). No modelling or machine learning — the dataset is clean and the questions are straightforward enough for descriptive and inferential statistics.

|  | Claim | Finding | Conclusion |
|--|-------|---------|------------|
| **H1** | Daily temps within 3°C | Average gap is 5.1°C; only 25% of days within threshold | Rejected |
| **H2** | Temperatures correlate day-to-day | r=0.81 daily, r=0.94 monthly | Confirmed |
| **H3** | Snow events co-occur | 2.6× more than chance | Weakly confirmed |
| **H4** | Sunny days co-occur | 1.4× more than chance | Weakly confirmed |

{% callout %}
The H1 rejection turned out to be the most interesting finding. The 5°C gap hid a seasonal story: it shrinks to just 4°C in winter (with some months where Bergen was actually warmer than Paris) and widens to 6°C in summer. This triggered an Analyse→Define loop — the original intuition of "similar temperatures" was probably specific to colder months, where the difference is least noticeable, and had been extrapolated to the whole year. The reframed question became: Bergen is not much colder than Paris when cold matters most (winter), and the gap in summer is actually a *feature* — Bergen avoids Paris's heatwaves entirely.
{% /callout %}

An additional threshold sensitivity lesson: Bergen "has snow 20% of days" using the raw model data (any snowfall >0mm), but that includes trace amounts from the reanalysis model. Using a 5mm+ threshold ("noticeable snow") gives 14% — which matched lived experience much better.

### Present

{% step-meta items="Tool: HTML / CSS / JavaScript, Charts: Chart.js, Maps: TopoJSON + Canvas, Data export: Python (export_for_web.py)" /%}

The goal was to help dispel a common misconception — especially among French people — that Norway is a country defined by snow and extreme cold. The site is structured in two parts: the *what* and the *why*.

The **what** explores the temperature comparison through both objective and subjective angles. The objective angle looks at the raw data: monthly averages, daily correlations, year-by-year heatmaps. The subjective angle reframes the gap as a lived experience: Bergen's snow days are warmer than you'd think, and its summers sit in the thermal comfort zone while Paris overshoots into heatwave territory.

The **why** explores geography — the distances between Bergen, Paris, and Tromsø — to explain why Bergen's climate is so different from the Arctic Norway people imagine. The Gulf Stream and Norway's sheer length are the key factors.

Many charts include a small interactive component to keep them engaging: filtering the heatmap by similarity level, scrubbing through years on the daily chart, or choosing a European capital on the flight distance map to make the "Norway is a long country" point personal and relatable.

The site is bilingual (EN/FR), auto-detecting French users, because the French audience is the primary one for this misconception.

## Tooling summary

The technical implementation was built with Claude Code, following a guardrail-first methodology: each task delegated to the LLM was bounded by a single pipeline phase, and its output was verified before moving to the next step. Every phase produced a verifiable artifact — a script, a dataset, a report — so the entire pipeline can be reproduced without any LLM involved, just by running the Python scripts in order. The methodological structure followed the [School of Data pipeline](https://civicliteraci.es/data-pipeline/), providing the framework that guided each step.

**Data pipeline** — five Python scripts, each handling one step:

```
fetch_data.py     → data/raw/           # Download from Open-Meteo API
verify_data.py                          # Sanity checks + cross-validation
clean_data.py     → data/clean/         # Merge and standardise
analyse.py                              # Test hypotheses
export_for_web.py → site/data/          # Export JSON for the website
```

**Website** — a single-page static site with no build step:

- [Chart.js](https://www.chartjs.org/) for interactive charts (lollipop, time series, scatter, bar)
- [TopoJSON](https://github.com/topojson/topojson-client) + HTML Canvas for the background map and flight distance map
- [Natural Earth / world-atlas](https://cdn.jsdelivr.net/npm/world-atlas@2) for country boundaries (50m resolution)
- Vanilla JavaScript for i18n, animated transitions, and computed statistics

**Publication** — hosted on GitHub Pages, served directly from the repository root. Source code at [github.com/clombion/bergen-paris-weather](https://github.com/clombion/bergen-paris-weather).

## Sources

**Data source** — [Open-Meteo Historical Weather API](https://open-meteo.com/) (ERA5 / ECMWF IFS reanalysis), 3,653 days of daily data per city. Snow days defined as days with 5mm+ snowfall. Thermal comfort zone based on [Cheung & Jim, 2019](https://link.springer.com/article/10.1007/s00484-019-01694-1).

**Project data** — the raw API responses and cleaned horizon table are stored in the repository for reproducibility:

- [data/raw/](https://github.com/clombion/bergen-paris-weather/tree/main/data/raw) — raw JSON from Open-Meteo (Bergen + Paris, 2016–2025)
- [data/clean/horizon.csv](https://github.com/clombion/bergen-paris-weather/blob/main/data/clean/horizon.csv) — the merged horizon table (3,653 rows × 13 columns)
- [site/data/](https://github.com/clombion/bergen-paris-weather/tree/main/site/data) — pre-computed JSON subsets powering the website charts
