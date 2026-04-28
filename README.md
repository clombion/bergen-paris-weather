# Bergen vs Paris Weather Comparison

**[Live site](https://clombion.github.io/bergen-paris-weather/)**

Bergen is not the frozen north you think it is. This project compares 10 years of daily weather data (2016–2025) between Bergen, Norway and Paris, France.

Key findings:
- Bergen is on average 5°C colder than Paris, but the gap shrinks to ~4°C in winter
- Daily temperatures are 81% correlated — when one city gets colder, so does the other
- Bergen's snow days average 1.5°C — almost eight in ten are above freezing
- Bergen is geographically closer to the French Riviera than to Arctic Norway
- When Paris bakes above 30°C (114 days over the decade), Bergen averages a comfortable 18°C

## The process

This project follows the [School of Data pipeline](https://civicliteraci.es/data-pipeline/) methodology: Define, Find, Get, Verify, Clean, Analyse, Present.

### Define

Started with a personal intuition: "Bergen and Paris weather are similar." We broke this into four testable hypotheses:

1. **H1**: Daily mean temperatures are within 3°C of each other
2. **H2**: Temperature changes correlate — when one city cools, so does the other
3. **H3**: Snow events co-occur more than chance would predict
4. **H4**: Sunny days co-occur more than chance would predict

### Find

Surveyed six data sources (Open-Meteo, Meteostat, Frost API, Météo-France, Visual Crossing, NOAA GSOD). Open-Meteo was the only one with all six required variables (temp mean/min/max, precipitation, snowfall, sunshine) for both cities at 100% completeness, with no API key needed.

### Get

Fetched 3,653 days of daily data per city from the Open-Meteo Historical Weather API (ERA5/ECMWF IFS reanalysis). Zero gaps, zero nulls.

### Verify

- **Completeness**: continuous date sequences, no missing values
- **Quality**: no temperatures outside plausible climate records, no negative precipitation, no suspicious flat-line periods
- **Cross-check**: compared ERA5 vs ECMWF IFS models. Paris data agrees within 1°C on 94% of days. Bergen shows ~1.6°C model uncertainty — noted but not disqualifying

### Clean

Merged both cities into a single horizon table (13 columns, daily granularity). Standardised units (sunshine to hours, snowfall to mm). Initially flagged extreme days (Paris >35°C, Bergen <-10°C) but a sensitivity check showed removing them changed results by <0.5°C, so we dropped the filtering.

Sample rows (subset of columns):

| date | bergen_temp_mean | paris_temp_mean | bergen_snowfall_mm | bergen_sunshine_hours |
|------|-----------------|----------------|-------------------|---------------------|
| 2016-01-01 | 3.6 | 6.5 | 18.2 | 3.64 |
| 2016-01-02 | 0.7 | 9.0 | 0.0 | 1.51 |
| 2016-01-03 | -2.7 | 6.9 | 0.0 | 5.18 |

Full table: 3,653 rows × 13 columns in `data/clean/horizon.csv`.

### Analyse

**H1 was rejected** — Bergen averages 5.1°C colder than Paris, not 3°C. Only 25% of days are within the threshold.

But that 5°C number turned out to be the most interesting finding. It wasn't as far from the hypothesised 3°C as it might sound, and it hid a seasonal story: the gap shrinks to just 4°C in winter (with some months where Bergen was actually warmer than Paris) and widens to 6°C in summer. This triggered an Analyse→Define loop — the original intuition of "similar temperatures" was probably specific to colder months, where the difference is least noticeable, and had been extrapolated to the whole year. The reframed question became: Bergen is not much colder than Paris when cold matters most (winter), and the gap in summer is actually a *feature* — Bergen avoids Paris's heatwaves entirely.

**H2 was confirmed** — r=0.81 daily correlation, r=0.94 monthly. They ride the same European weather systems.

**H3 and H4 were weakly confirmed** — snow co-occurs 2.6× more than chance, sunny days 1.4×.

An additional threshold sensitivity lesson: Bergen "has snow 20% of days" using the raw model data (any snowfall >0mm), but that includes trace amounts from the reanalysis model. Using a 5mm+ threshold ("noticeable snow") gives 14% — which matched lived experience much better. The core stats (temperature on snow days, comfort gaps) barely changed with the threshold, but the headline number needed to be credible.

### Present

The goal was to help dispel a common misconception — especially among French people — that Norway is a country defined by snow and extreme cold. The site is structured in two parts: the *what* and the *why*.

The **what** explores the temperature comparison through both objective and subjective angles. The objective angle looks at the raw data: monthly averages, daily correlations, year-by-year heatmaps. The subjective angle reframes the gap as a lived experience: Bergen's snow days are warmer than you'd think, and its summers sit in the thermal comfort zone while Paris overshoots into heatwave territory.

The **why** explores geography — the distances between Bergen, Paris, and Tromsø — to explain why Bergen's climate is so different from the Arctic Norway people imagine. The Gulf Stream and Norway's sheer length are the key factors.

Many charts include a small interactive component to keep them engaging: filtering the heatmap by similarity level, scrubbing through years on the daily chart, or choosing a European capital on the flight distance map to make the "Norway is a long country" point personal and relatable.

The site is bilingual (EN/FR), auto-detecting French users, because the French audience is the primary one for this misconception.

## Pipeline scripts

```
fetch_data.py     → data/raw/           # Download from Open-Meteo
verify_data.py                          # Sanity checks + cross-validation
clean_data.py     → data/clean/         # Merge and standardise
analyse.py                              # Test hypotheses
export_for_web.py → site/data/          # Export JSON for the website
```

## Build the site

Content lives in Markdown files (`content/en/`, `content/fr/`) using [Markdoc](https://markdoc.dev/) custom tags. A build script renders them into static HTML.

```bash
pnpm install
pnpm run build
```

The build outputs to `dist/`. To preview locally:

```bash
pnpm exec serve dist
```

## Run the data pipeline

```bash
python3 fetch_data.py
python3 clean_data.py
python3 export_for_web.py
```

## Data

Source: [Open-Meteo Historical Weather API](https://open-meteo.com/) (ERA5 / ECMWF IFS reanalysis), 3,653 days of daily data. Snow days defined as days with 5mm+ snowfall.

## License

Data: [Open-Meteo](https://open-meteo.com/) (CC BY 4.0). Code: MIT.
