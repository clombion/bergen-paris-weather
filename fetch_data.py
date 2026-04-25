"""Fetch daily weather data for Bergen and Paris from Open-Meteo Historical API."""

import json
import urllib.request
from datetime import datetime
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

CITIES = {
    "bergen": {"latitude": 60.39, "longitude": 5.32},
    "paris": {"latitude": 48.86, "longitude": 2.35},
}

DAILY_VARS = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "snowfall_sum",
    "sunshine_duration",
]

START_DATE = "2016-01-01"
END_DATE = "2025-12-31"


def fetch_city(name: str, coords: dict) -> dict:
    params = (
        f"latitude={coords['latitude']}"
        f"&longitude={coords['longitude']}"
        f"&start_date={START_DATE}"
        f"&end_date={END_DATE}"
        f"&daily={','.join(DAILY_VARS)}"
        f"&timezone=auto"
    )
    url = f"https://archive-api.open-meteo.com/v1/archive?{params}"

    print(f"Fetching {name}...")
    print(f"  URL: {url}")

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())

    # Add provenance metadata
    data["_provenance"] = {
        "city": name,
        "fetched_at": datetime.now().isoformat(),
        "source": "Open-Meteo Historical Weather API",
        "url": url,
    }

    n_days = len(data["daily"]["time"])
    print(f"  Got {n_days} days ({data['daily']['time'][0]} to {data['daily']['time'][-1]})")

    # Check for nulls in each variable
    for var in DAILY_VARS:
        nulls = sum(1 for v in data["daily"][var] if v is None)
        if nulls:
            print(f"  WARNING: {var} has {nulls} null values ({nulls/n_days*100:.1f}%)")
        else:
            print(f"  {var}: complete")

    return data


def main():
    for name, coords in CITIES.items():
        data = fetch_city(name, coords)
        out_path = RAW_DIR / f"{name}.json"
        with open(out_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Saved to {out_path}\n")

    print("Done. Raw data saved to data/raw/")


if __name__ == "__main__":
    main()
