"""Analyse the horizon table against all four hypotheses."""

import csv
import math
from collections import defaultdict

def load_horizon(exclude_extremes=False):
    rows = []
    with open("data/clean/horizon.csv") as f:
        for row in csv.DictReader(f):
            if exclude_extremes and row["extreme"] == "True":
                continue
            # Convert types
            for k in row:
                if k == "date" or k == "extreme":
                    continue
                row[k] = float(row[k])
            rows.append(row)
    return rows


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0
    return num / (dx * dy)


def percentile(vals, p):
    s = sorted(vals)
    k = (len(s) - 1) * p / 100
    f = int(k)
    c = f + 1 if f + 1 < len(s) else f
    return s[f] + (k - f) * (s[c] - s[f])


def analyse_h1(rows, label):
    """H1: Are daily mean temperatures within 3°C?"""
    diffs = [r["bergen_temp_mean"] - r["paris_temp_mean"] for r in rows]
    abs_diffs = [abs(d) for d in diffs]
    n = len(diffs)

    mean_diff = sum(diffs) / n
    median_diff = percentile(diffs, 50)
    mean_abs = sum(abs_diffs) / n
    median_abs = percentile(abs_diffs, 50)

    within_1 = sum(1 for d in abs_diffs if d <= 1)
    within_2 = sum(1 for d in abs_diffs if d <= 2)
    within_3 = sum(1 for d in abs_diffs if d <= 3)
    within_5 = sum(1 for d in abs_diffs if d <= 5)

    print(f"\n  H1: Temperature Difference ({label}, n={n})")
    print(f"  {'─'*50}")
    print(f"  Bergen is on average {abs(mean_diff):.1f}°C {'colder' if mean_diff < 0 else 'warmer'} than Paris")
    print(f"  Mean difference (Bergen - Paris): {mean_diff:+.1f}°C")
    print(f"  Median difference: {median_diff:+.1f}°C")
    print(f"  Mean absolute difference: {mean_abs:.1f}°C")
    print(f"  Median absolute difference: {median_abs:.1f}°C")
    print(f"  P10-P90 range: {percentile(diffs, 10):+.1f} to {percentile(diffs, 90):+.1f}°C")
    print(f"  Within 1°C: {within_1}/{n} ({within_1/n*100:.0f}%)")
    print(f"  Within 2°C: {within_2}/{n} ({within_2/n*100:.0f}%)")
    print(f"  Within 3°C: {within_3}/{n} ({within_3/n*100:.0f}%)")
    print(f"  Within 5°C: {within_5}/{n} ({within_5/n*100:.0f}%)")

    # Seasonal breakdown
    print(f"\n  By season:")
    seasons = {"Winter (DJF)": [12,1,2], "Spring (MAM)": [3,4,5],
               "Summer (JJA)": [6,7,8], "Autumn (SON)": [9,10,11]}
    for name, months in seasons.items():
        s_diffs = [r["bergen_temp_mean"] - r["paris_temp_mean"]
                   for r in rows if int(r["date"].split("-")[1]) in months]
        if s_diffs:
            s_mean = sum(s_diffs) / len(s_diffs)
            s_abs = sum(abs(d) for d in s_diffs) / len(s_diffs)
            s_w3 = sum(1 for d in s_diffs if abs(d) <= 3)
            print(f"    {name}: mean diff {s_mean:+.1f}°C, "
                  f"mean |diff| {s_abs:.1f}°C, "
                  f"within 3°C: {s_w3/len(s_diffs)*100:.0f}%")

    return mean_diff, median_abs


def analyse_h2(rows, label):
    """H2: Do temperatures correlate / co-move?"""
    bergen = [r["bergen_temp_mean"] for r in rows]
    paris = [r["paris_temp_mean"] for r in rows]

    # Same-day correlation
    r0 = pearson(bergen, paris)

    # Lag correlations (Bergen leads Paris by N days, and vice versa)
    print(f"\n  H2: Temperature Correlation ({label}, n={len(rows)})")
    print(f"  {'─'*50}")
    print(f"  Same-day correlation (r): {r0:.3f}")

    for lag in [1, 2, 3]:
        # Bergen[t] vs Paris[t+lag] — does Bergen predict Paris?
        r_bp = pearson(bergen[:-lag], paris[lag:])
        # Paris[t] vs Bergen[t+lag] — does Paris predict Bergen?
        r_pb = pearson(paris[:-lag], bergen[lag:])
        print(f"  Lag {lag}d: Bergen→Paris r={r_bp:.3f}, Paris→Bergen r={r_pb:.3f}")

    # Daily change correlation
    bergen_delta = [bergen[i] - bergen[i-1] for i in range(1, len(bergen))]
    paris_delta = [paris[i] - paris[i-1] for i in range(1, len(paris))]
    r_delta = pearson(bergen_delta, paris_delta)
    print(f"  Daily change correlation (Δtemp): {r_delta:.3f}")

    # Monthly mean correlation
    monthly = defaultdict(lambda: {"bergen": [], "paris": []})
    for r in rows:
        ym = r["date"][:7]
        monthly[ym]["bergen"].append(r["bergen_temp_mean"])
        monthly[ym]["paris"].append(r["paris_temp_mean"])

    b_monthly = [sum(v["bergen"])/len(v["bergen"]) for v in monthly.values()]
    p_monthly = [sum(v["paris"])/len(v["paris"]) for v in monthly.values()]
    r_monthly = pearson(b_monthly, p_monthly)
    print(f"  Monthly mean correlation: {r_monthly:.3f}")

    return r0, r_delta


def analyse_h3(rows, label):
    """H3: Snow co-occurrence vs chance."""
    n = len(rows)
    bergen_snow = [r["bergen_snowfall_mm"] > 0 for r in rows]
    paris_snow = [r["paris_snowfall_mm"] > 0 for r in rows]

    b_count = sum(bergen_snow)
    p_count = sum(paris_snow)
    both = sum(b and p for b, p in zip(bergen_snow, paris_snow))

    b_rate = b_count / n
    p_rate = p_count / n
    expected_both = b_rate * p_rate * n
    actual_ratio = both / expected_both if expected_both > 0 else float('inf')

    print(f"\n  H3: Snow Co-occurrence ({label}, n={n})")
    print(f"  {'─'*50}")
    print(f"  Bergen snow days: {b_count} ({b_rate*100:.1f}%)")
    print(f"  Paris snow days: {p_count} ({p_rate*100:.1f}%)")
    print(f"  Both snow same day: {both}")
    print(f"  Expected by chance: {expected_both:.1f}")
    print(f"  Actual / expected: {actual_ratio:.1f}x")
    print(f"  Verdict: {'MORE than chance' if actual_ratio > 1.5 else 'CLOSE TO chance' if actual_ratio > 0.7 else 'LESS than chance'}")

    # When Paris has snow, how often does Bergen?
    if p_count > 0:
        p_given_paris = sum(b and p for b, p in zip(bergen_snow, paris_snow)) / p_count
        print(f"  P(Bergen snow | Paris snow): {p_given_paris*100:.0f}%")
    if b_count > 0:
        p_given_bergen = sum(b and p for b, p in zip(bergen_snow, paris_snow)) / b_count
        print(f"  P(Paris snow | Bergen snow): {p_given_bergen*100:.0f}%")

    return both, expected_both


def analyse_h4(rows, label):
    """H4: Sunny day co-occurrence vs chance."""
    n = len(rows)
    # Define "sunny" as above-median sunshine for each city
    b_sun = [r["bergen_sunshine_hours"] for r in rows]
    p_sun = [r["paris_sunshine_hours"] for r in rows]

    # Also try a fixed threshold: >8 hours
    threshold = 8
    bergen_sunny = [s > threshold for s in b_sun]
    paris_sunny = [s > threshold for s in p_sun]

    b_count = sum(bergen_sunny)
    p_count = sum(paris_sunny)
    both = sum(b and p for b, p in zip(bergen_sunny, paris_sunny))

    b_rate = b_count / n
    p_rate = p_count / n
    expected_both = b_rate * p_rate * n
    actual_ratio = both / expected_both if expected_both > 0 else float('inf')

    print(f"\n  H4: Sunny Day Co-occurrence ({label}, n={n}, threshold={threshold}h)")
    print(f"  {'─'*50}")
    print(f"  Bergen sunny days (>{threshold}h): {b_count} ({b_rate*100:.1f}%)")
    print(f"  Paris sunny days (>{threshold}h): {p_count} ({p_rate*100:.1f}%)")
    print(f"  Both sunny same day: {both}")
    print(f"  Expected by chance: {expected_both:.1f}")
    print(f"  Actual / expected: {actual_ratio:.1f}x")
    print(f"  Verdict: {'MORE than chance' if actual_ratio > 1.5 else 'CLOSE TO chance' if actual_ratio > 0.7 else 'LESS than chance'}")

    # Sunshine correlation
    r_sun = pearson(b_sun, p_sun)
    print(f"  Sunshine hours correlation (r): {r_sun:.3f}")

    # Also check: both overcast (<2h)
    b_grey = [s < 2 for s in b_sun]
    p_grey = [s < 2 for s in p_sun]
    both_grey = sum(b and p for b, p in zip(b_grey, p_grey))
    b_grey_n = sum(b_grey)
    p_grey_n = sum(p_grey)
    exp_grey = (b_grey_n / n) * (p_grey_n / n) * n
    grey_ratio = both_grey / exp_grey if exp_grey > 0 else float('inf')
    print(f"  Both overcast (<2h): {both_grey} (expected {exp_grey:.0f}, ratio {grey_ratio:.1f}x)")

    return both, expected_both


def main():
    for exclude, label in [(False, "all days"), (True, "excl. extremes")]:
        rows = load_horizon(exclude_extremes=exclude)
        print(f"\n{'='*60}")
        print(f"  ANALYSIS: {label.upper()} (n={len(rows)})")
        print(f"{'='*60}")

        analyse_h1(rows, label)
        analyse_h2(rows, label)
        analyse_h3(rows, label)
        analyse_h4(rows, label)

    # Final verdict
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
