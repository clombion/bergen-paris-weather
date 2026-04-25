"""Verify fetched Open-Meteo data: completeness, outliers, and cross-check against Meteostat JSON API."""

import json
import urllib.request
from datetime import date, timedelta


# --- 1. Completeness: check for date gaps and null values ---

def check_completeness(city: str, daily: dict):
    dates = daily["time"]
    n = len(dates)
    print(f"\n{'='*60}")
    print(f"COMPLETENESS: {city.upper()}")
    print(f"{'='*60}")
    print(f"  Total days: {n}")
    print(f"  Range: {dates[0]} to {dates[-1]}")

    # Check for date gaps
    expected = date.fromisoformat(dates[0])
    gaps = []
    for d in dates:
        actual = date.fromisoformat(d)
        if actual != expected:
            gaps.append((expected, actual))
        expected = actual + timedelta(days=1)

    if gaps:
        print(f"  DATE GAPS FOUND: {len(gaps)}")
        for start, end in gaps[:5]:
            print(f"    Missing: {start} to {end - timedelta(days=1)}")
    else:
        print(f"  No date gaps - continuous sequence")

    expected_days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days + 1
    print(f"  Expected days: {expected_days}, actual: {n}, match: {n == expected_days}")

    # Check for nulls per variable
    vars_to_check = [
        "temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
        "precipitation_sum", "snowfall_sum", "sunshine_duration",
    ]
    for var in vars_to_check:
        nulls = sum(1 for v in daily[var] if v is None)
        print(f"  {var}: {nulls} nulls ({nulls/n*100:.1f}%)")


# --- 2. Quality: outlier and range checks ---

def check_quality(city: str, daily: dict):
    print(f"\n{'='*60}")
    print(f"QUALITY: {city.upper()}")
    print(f"{'='*60}")

    temps = daily["temperature_2m_mean"]
    temp_min = daily["temperature_2m_min"]
    temp_max = daily["temperature_2m_max"]
    precip = daily["precipitation_sum"]
    snow = daily["snowfall_sum"]
    dates = daily["time"]

    # Temperature sanity: mean should be between min and max
    violations = []
    for i, (mn, avg, mx) in enumerate(zip(temp_min, temps, temp_max)):
        if avg < mn - 0.5 or avg > mx + 0.5:
            violations.append((dates[i], mn, avg, mx))
    print(f"  Temp mean outside min/max range: {len(violations)} days")
    for d, mn, avg, mx in violations[:3]:
        print(f"    {d}: min={mn} mean={avg} max={mx}")

    # Temperature range check (known climate records)
    KNOWN_RANGES = {
        "bergen": (-25, 35),
        "paris": (-20, 45),
    }
    lo, hi = KNOWN_RANGES[city]
    extremes = [(dates[i], temp_min[i], temp_max[i])
                for i in range(len(dates))
                if temp_min[i] < lo or temp_max[i] > hi]
    print(f"  Temps outside plausible range [{lo}, {hi}]°C: {len(extremes)}")

    # Negative precipitation/snowfall
    neg_precip = sum(1 for v in precip if v < 0)
    neg_snow = sum(1 for v in snow if v < 0)
    print(f"  Negative precipitation: {neg_precip} days")
    print(f"  Negative snowfall: {neg_snow} days")

    # Suspicious flat-line: >7 consecutive identical mean temps
    flat_runs = []
    run_start = 0
    for i in range(1, len(temps)):
        if temps[i] != temps[run_start]:
            if i - run_start > 7:
                flat_runs.append((dates[run_start], dates[i-1], i - run_start, temps[run_start]))
            run_start = i
    print(f"  Flat-line periods (>7 days same mean temp): {len(flat_runs)}")
    for start, end, length, val in flat_runs[:3]:
        print(f"    {start} to {end}: {length} days at {val}°C")

    # Snow in summer check
    summer_snow = [(dates[i], snow[i]) for i in range(len(dates))
                   if date.fromisoformat(dates[i]).month in (6, 7, 8) and snow[i] > 0]
    print(f"  Summer (Jun-Aug) snow days: {len(summer_snow)}")
    for d, s in summer_snow[:3]:
        print(f"    {d}: {s} cm")


# --- 3. Cross-check: compare 2023 mean temps against Meteostat JSON API ---

def cross_check_meteostat():
    """Compare 2023 mean temperatures against Meteostat station data via their public JSON API."""
    print(f"\n{'='*60}")
    print(f"CROSS-CHECK: Open-Meteo vs Meteostat (2023)")
    print(f"{'='*60}")

    # Meteostat station IDs
    station_checks = {
        "bergen": "01317",   # Bergen / Florida
        "paris": "07156",    # Paris-Montsouris
    }

    for city, station_id in station_checks.items():
        # Load Open-Meteo data for 2023
        with open(f"data/raw/{city}.json") as f:
            om = json.load(f)["daily"]

        om_2023 = {
            om["time"][i]: om["temperature_2m_mean"][i]
            for i in range(len(om["time"]))
            if om["time"][i].startswith("2023-")
        }

        # Fetch from Meteostat JSON API
        url = (
            f"https://meteostat.p.rapidapi.com/stations/daily"
            f"?station={station_id}&start=2023-01-01&end=2023-12-31"
        )

        # Meteostat public bulk data (no API key needed)
        bulk_url = f"https://bulk.meteostat.net/v2/stations/daily/{station_id}.csv.gz"
        print(f"\n  {city.upper()}: Fetching station {station_id} from Meteostat bulk...")

        try:
            req = urllib.request.Request(bulk_url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                import gzip, csv, io
                raw = gzip.decompress(resp.read()).decode("utf-8")
                reader = csv.reader(io.StringIO(raw))
                # Columns: date,tavg,tmin,tmax,prcp,snow,wdir,wspd,wpgt,pres,tsun
                ms_temps = {}
                for row in reader:
                    if row[0].startswith("2023-") and row[1]:
                        try:
                            ms_temps[row[0]] = float(row[1])
                        except ValueError:
                            pass

            if not ms_temps:
                print(f"    No 2023 tavg data found in Meteostat bulk data")
                continue

            matched = 0
            diffs = []
            for d_str, ms_val in ms_temps.items():
                if d_str in om_2023:
                    diff = om_2023[d_str] - ms_val
                    diffs.append(diff)
                    matched += 1

            if not diffs:
                print(f"    No overlapping days found")
                continue

            avg_diff = sum(diffs) / len(diffs)
            abs_diffs = [abs(d) for d in diffs]
            max_diff = max(abs_diffs)
            within_1 = sum(1 for d in abs_diffs if d <= 1.0)
            within_2 = sum(1 for d in abs_diffs if d <= 2.0)

            print(f"    Matched {matched} days")
            print(f"    Mean difference (Open-Meteo - Meteostat): {avg_diff:+.2f}°C")
            print(f"    Max absolute difference: {max_diff:.2f}°C")
            print(f"    Within 1°C: {within_1}/{matched} ({within_1/matched*100:.0f}%)")
            print(f"    Within 2°C: {within_2}/{matched} ({within_2/matched*100:.0f}%)")

        except Exception as e:
            print(f"    Could not fetch Meteostat data: {e}")


def main():
    for city in ["bergen", "paris"]:
        with open(f"data/raw/{city}.json") as f:
            data = json.load(f)
        check_completeness(city, data["daily"])
        check_quality(city, data["daily"])

    cross_check_meteostat()

    print(f"\n{'='*60}")
    print("VERIFICATION COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
