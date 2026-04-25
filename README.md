# Bergen vs Paris Weather Comparison

**[Live site](https://clombion.github.io/bergen-paris-weather/)**

Bergen is not the frozen north you think it is. This project compares 10 years of daily weather data (2016–2025) between Bergen, Norway and Paris, France.

Key findings:
- Bergen is on average 5°C colder than Paris, but the gap shrinks to ~4°C in winter
- Daily temperatures are 81% correlated — when one city gets colder, so does the other
- Bergen's snow days average 1.5°C — almost eight in ten are above freezing
- Bergen is geographically closer to the French Riviera than to Arctic Norway

## Data

Source: [Open-Meteo Historical Weather API](https://open-meteo.com/) (ERA5 / ECMWF IFS reanalysis), 3,653 days of daily data.

## Pipeline

This project follows the [School of Data pipeline](https://civicliteraci.es/data-pipeline/) methodology: Define, Find, Get, Verify, Clean, Analyse, Present.

```
fetch_data.py    → data/raw/           # Download from Open-Meteo
verify_data.py                         # Sanity checks + cross-validation
clean_data.py    → data/clean/         # Merge, standardize, flag extremes
analyse.py                             # Test hypotheses
export_for_web.py → docs/data/         # Export JSON for the site
```

## Run locally

```bash
python3 fetch_data.py
python3 clean_data.py
python3 export_for_web.py
python3 -m http.server 8080 --directory docs
```

## License

Data: [Open-Meteo](https://open-meteo.com/) (CC BY 4.0). Code: MIT.
