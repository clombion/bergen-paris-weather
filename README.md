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

### Analyse

**H1 was rejected** — Bergen averages 5.1°C colder than Paris, not 3°C. Only 25% of days are within the threshold.

But that 5°C number turned out to be the most interesting finding. It wasn't as far from the hypothesised 3°C as it might sound, and it hid a seasonal story: the gap shrinks to just 4°C in winter (with some months where Bergen was actually warmer than Paris) and widens to 6°C in summer. This triggered an Analyse→Define loop — the original intuition of "similar temperatures" was probably specific to colder months, where the difference is least noticeable, and had been extrapolated to the whole year. The reframed question became: Bergen is not much colder than Paris when cold matters most (winter), and the gap in summer is actually a *feature* — Bergen avoids Paris's heatwaves entirely.

**H2 was confirmed** — r=0.81 daily correlation, r=0.94 monthly. They ride the same European weather systems.

**H3 and H4 were weakly confirmed** — snow co-occurs 2.6× more than chance, sunny days 1.4×.

An additional threshold sensitivity lesson: Bergen "has snow 20% of days" using the raw model data (any snowfall >0mm), but that includes trace amounts from the reanalysis model. Using a 5mm+ threshold ("noticeable snow") gives 14% — which matched lived experience much better. The core stats (temperature on snow days, comfort gaps) barely changed with the threshold, but the headline number needed to be credible.

### Present

The goal was to help dispel a common misconception — especially among French people — that Norway is a country defined by snow and extreme cold. The site is designed as a narrative that progressively challenges that assumption: winters are milder than expected, snow days are barely below freezing, summers avoid heatwaves, and the "frozen Norway" people picture is actually Tromsø, over 1,200 km from Bergen.

The site is bilingual (EN/FR), auto-detecting French users, because the French audience is the primary one for this misconception. An interactive flight distance map lets visitors compare Bergen–Tromsø with Bergen to their own European capital, making the "Norway is a long country" point personal and concrete.

## Pipeline scripts

```
fetch_data.py     → data/raw/           # Download from Open-Meteo
verify_data.py                          # Sanity checks + cross-validation
clean_data.py     → data/clean/         # Merge and standardise
analyse.py                              # Test hypotheses
export_for_web.py → site/data/          # Export JSON for the website
```

## Run locally

```bash
python3 fetch_data.py
python3 clean_data.py
python3 export_for_web.py
python3 -m http.server 8080
```

## Data

Source: [Open-Meteo Historical Weather API](https://open-meteo.com/) (ERA5 / ECMWF IFS reanalysis), 3,653 days of daily data. Snow days defined as days with 5mm+ snowfall.

## License

Data: [Open-Meteo](https://open-meteo.com/) (CC BY 4.0). Code: MIT.
