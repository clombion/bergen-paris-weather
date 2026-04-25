"""Clean and merge raw weather data into the horizon table CSV."""

import csv
import json
from pathlib import Path

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/clean")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_raw(city: str) -> dict:
    with open(RAW_DIR / f"{city}.json") as f:
        return json.load(f)["daily"]


def main():
    bergen = load_raw("bergen")
    paris = load_raw("paris")

    assert bergen["time"] == paris["time"], "Date sequences don't match"

    dates = bergen["time"]
    rows = []

    for i, d in enumerate(dates):
        bergen_sun_h = round(bergen["sunshine_duration"][i] / 3600, 2)
        paris_sun_h = round(paris["sunshine_duration"][i] / 3600, 2)
        bergen_snow_mm = round(bergen["snowfall_sum"][i] * 10, 1)  # cm -> mm
        paris_snow_mm = round(paris["snowfall_sum"][i] * 10, 1)

        # Flag extremes: Paris heatwaves (>35°C) or Bergen deep cold (<-10°C)
        extreme = False
        if paris["temperature_2m_max"][i] > 35:
            extreme = True
        if bergen["temperature_2m_min"][i] < -10:
            extreme = True

        rows.append({
            "date": d,
            "bergen_temp_mean": bergen["temperature_2m_mean"][i],
            "paris_temp_mean": paris["temperature_2m_mean"][i],
            "bergen_temp_min": bergen["temperature_2m_min"][i],
            "paris_temp_min": paris["temperature_2m_min"][i],
            "bergen_temp_max": bergen["temperature_2m_max"][i],
            "paris_temp_max": paris["temperature_2m_max"][i],
            "bergen_precip_mm": bergen["precipitation_sum"][i],
            "paris_precip_mm": paris["precipitation_sum"][i],
            "bergen_snowfall_mm": bergen_snow_mm,
            "paris_snowfall_mm": paris_snow_mm,
            "bergen_sunshine_hours": bergen_sun_h,
            "paris_sunshine_hours": paris_sun_h,
            "extreme": extreme,
        })

    # Write CSV
    out_path = OUT_DIR / "horizon.csv"
    fieldnames = list(rows[0].keys())
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Summary
    n = len(rows)
    n_extreme = sum(1 for r in rows if r["extreme"])
    print(f"Horizon table: {n} rows, {len(fieldnames)} columns")
    print(f"Extreme days flagged: {n_extreme} ({n_extreme/n*100:.1f}%)")
    print(f"  Paris >35°C: {sum(1 for r in rows if r['paris_temp_max'] > 35)}")
    print(f"  Bergen <-10°C: {sum(1 for r in rows if r['bergen_temp_min'] < -10)}")
    print(f"Saved to {out_path}")

    # Quick sanity: print first 3 rows
    print(f"\nFirst 3 rows:")
    for r in rows[:3]:
        print(f"  {r['date']}: Bergen {r['bergen_temp_mean']}°C, Paris {r['paris_temp_mean']}°C, extreme={r['extreme']}")


if __name__ == "__main__":
    main()
