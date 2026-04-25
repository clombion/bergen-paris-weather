"""Export cleaned data and analysis results as JSON for the website."""

import csv
import json
from collections import defaultdict
from pathlib import Path

OUT = Path("site/data")
OUT.mkdir(parents=True, exist_ok=True)


def load():
    rows = []
    with open("data/clean/horizon.csv") as f:
        for r in csv.DictReader(f):
            for k in r:
                if k in ("date", "extreme"):
                    continue
                r[k] = float(r[k])
            r["extreme"] = r["extreme"] == "True"
            rows.append(r)
    return rows


def export_daily(rows):
    """Daily data — dates and key temps only (keep payload small)."""
    daily = {
        "dates": [r["date"] for r in rows],
        "bergen_mean": [r["bergen_temp_mean"] for r in rows],
        "paris_mean": [r["paris_temp_mean"] for r in rows],
        "bergen_min": [r["bergen_temp_min"] for r in rows],
        "paris_min": [r["paris_temp_min"] for r in rows],
        "bergen_max": [r["bergen_temp_max"] for r in rows],
        "paris_max": [r["paris_temp_max"] for r in rows],
        "bergen_snow": [r["bergen_snowfall_mm"] for r in rows],
        "paris_snow": [r["paris_snowfall_mm"] for r in rows],
        "bergen_sun": [r["bergen_sunshine_hours"] for r in rows],
        "paris_sun": [r["paris_sunshine_hours"] for r in rows],
        "extreme": [r["extreme"] for r in rows],
    }
    with open(OUT / "daily.json", "w") as f:
        json.dump(daily, f)
    print(f"daily.json: {len(rows)} days")


def export_monthly_summary(rows):
    """Monthly pooled averages and gap stats."""
    monthly = defaultdict(lambda: {"bergen": [], "paris": [], "diffs": []})
    for r in rows:
        m = int(r["date"].split("-")[1])
        monthly[m]["bergen"].append(r["bergen_temp_mean"])
        monthly[m]["paris"].append(r["paris_temp_mean"])
        monthly[m]["diffs"].append(r["bergen_temp_mean"] - r["paris_temp_mean"])

    result = []
    for m in range(1, 13):
        d = monthly[m]
        n = len(d["diffs"])
        abs_diffs = [abs(x) for x in d["diffs"]]
        result.append({
            "month": m,
            "bergen_mean": round(sum(d["bergen"]) / n, 1),
            "paris_mean": round(sum(d["paris"]) / n, 1),
            "mean_diff": round(sum(d["diffs"]) / n, 1),
            "mean_abs_diff": round(sum(abs_diffs) / n, 1),
            "within_3c_pct": round(sum(1 for x in abs_diffs if x <= 3) / n * 100),
        })

    with open(OUT / "monthly.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"monthly.json: 12 months")


def export_year_month(rows):
    """Year x month grid of mean differences."""
    ym = defaultdict(list)
    for r in rows:
        y, m = r["date"].split("-")[0], int(r["date"].split("-")[1])
        ym[(y, m)].append(r["bergen_temp_mean"] - r["paris_temp_mean"])

    result = []
    for y in range(2016, 2026):
        for m in range(1, 13):
            d = ym.get((str(y), m), [])
            if d:
                result.append({
                    "year": y,
                    "month": m,
                    "mean_diff": round(sum(d) / len(d), 1),
                })

    with open(OUT / "year_month.json", "w") as f:
        json.dump(result, f)
    print(f"year_month.json: {len(result)} entries")


def export_surprise_months(rows):
    """Months where Bergen was within 3°C or warmer than Paris."""
    ym = defaultdict(list)
    for r in rows:
        y, m = r["date"].split("-")[0], int(r["date"].split("-")[1])
        ym[(y, m)].append(r["bergen_temp_mean"] - r["paris_temp_mean"])

    surprises = []
    for (y, m), diffs in sorted(ym.items()):
        mean = sum(diffs) / len(diffs)
        if abs(mean) < 3:
            surprises.append({
                "year": int(y), "month": m,
                "mean_diff": round(mean, 1),
                "warmer": mean > 0,
            })

    with open(OUT / "surprises.json", "w") as f:
        json.dump(surprises, f, indent=2)
    print(f"surprises.json: {len(surprises)} surprise months")


def main():
    rows = load()
    export_daily(rows)
    export_monthly_summary(rows)
    export_year_month(rows)
    export_surprise_months(rows)
    print("Done.")


if __name__ == "__main__":
    main()
