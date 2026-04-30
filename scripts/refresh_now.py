"""Fetch current weather for Bergen and Paris and write a JSON snapshot.

Run hourly via .github/workflows/refresh-weather.yml. Writes to the path
given as the first CLI argument (default: site/data/now.json). The snapshot
is consumed by the live-legend tag's client JS, which falls back to the
bare legend if the file is missing or older than 6 hours.

Stdlib-only — no dependencies, no pip install in CI.
"""

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CITIES = [
    {"name": "Bergen", "lat": 60.39, "lon": 5.32},
    {"name": "Paris", "lat": 48.86, "lon": 2.35},
]

# WMO weather code → emoji. Codes that map to a single Unicode codepoint
# in the BMP (☀ ☁ ❄ ⛅ ⛈) need VS-16 (️) appended to force emoji
# presentation; without it they render as monochrome text glyphs.
SUN = "☀️"
CLOUD = "☁️"
SNOW_BMP = "❄️"
PARTLY = "⛅"
PARTLY_DAY = "\U0001f324️"  # 🌤️ — emoji default, but VS-16 is harmless
THUNDER = "⛈️"
MOON = "\U0001f319"
FOG = "\U0001f32b️"
DRIZZLE = "\U0001f326️"
RAIN = "\U0001f327️"
SNOW = "\U0001f328️"

# Day-only codes: same icon regardless of is_day. The codes that vary
# between day and night (clear / mainly clear / partly cloudy) are
# handled in icon_for().
WMO_ICON = {
    3: CLOUD,
    45: FOG, 48: FOG,
    51: DRIZZLE, 53: DRIZZLE, 55: RAIN,
    56: RAIN, 57: RAIN,
    61: DRIZZLE, 63: RAIN, 65: RAIN,
    66: RAIN, 67: RAIN,
    71: SNOW, 73: SNOW, 75: SNOW_BMP,
    77: SNOW,
    80: DRIZZLE, 81: RAIN, 82: THUNDER,
    85: SNOW, 86: SNOW,
    95: THUNDER, 96: THUNDER, 99: THUNDER,
}


def icon_for(code: int, is_day: int) -> str:
    code = int(code)
    night = not is_day
    if code == 0:
        return MOON if night else SUN
    if code == 1:
        return MOON if night else PARTLY_DAY
    if code == 2:
        return CLOUD if night else PARTLY
    return WMO_ICON.get(code, "•")


def fetch_current() -> list[dict]:
    lats = ",".join(str(c["lat"]) for c in CITIES)
    lons = ",".join(str(c["lon"]) for c in CITIES)
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lats}&longitude={lons}"
        "&current=temperature_2m,weather_code,is_day&timezone=auto"
    )
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode())


def format_temp(t: float) -> str:
    return f"{round(t)}°C"


def summary_strings(bergen_t: float, paris_t: float) -> dict:
    delta = paris_t - bergen_t
    if delta < 0:
        return {
            "en": "Bergen is warmer than Paris today",
            "fr": "Bergen est plus chaud que Paris aujourd'hui",
        }
    rounded = round(abs(delta))
    if abs(delta) < 4:
        en_tail = "smaller than the decade average of 5°C"
        fr_tail = "plus faible que la moyenne décennale de 5°C"
    elif abs(delta) <= 6:
        en_tail = "about the same as the decade average of 5°C"
        fr_tail = "comparable à la moyenne décennale de 5°C"
    else:
        en_tail = "larger than the decade average of 5°C"
        fr_tail = "plus grand que la moyenne décennale de 5°C"
    return {
        "en": f"{rounded}°C gap today — {en_tail}",
        "fr": f"Écart de {rounded}°C aujourd'hui — {fr_tail}",
    }


def build_snapshot(api_data: list[dict]) -> dict:
    items = {}
    temps = {}
    for city, entry in zip(CITIES, api_data):
        cur = entry["current"]
        items[city["name"]] = {
            "value": format_temp(cur["temperature_2m"]),
            "icon": icon_for(cur["weather_code"], cur.get("is_day", 1)),
        }
        temps[city["name"]] = cur["temperature_2m"]

    return {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": items,
        "summary": summary_strings(temps["Bergen"], temps["Paris"]),
    }


def main(out_path: str) -> int:
    api_data = fetch_current()
    snapshot = build_snapshot(api_data)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Skip writing if items+summary unchanged. The `updated` field would
    # otherwise differ on every run, churning the data branch with no-op
    # commits and triggering deploys that change nothing visible.
    if out.exists():
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
            same = (
                existing.get("items") == snapshot["items"]
                and existing.get("summary") == snapshot["summary"]
            )
            if same:
                print(f"unchanged, skipping write: {out}")
                return 0
        except (json.JSONDecodeError, OSError):
            pass

    out.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote: {out}")
    return 0


if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "site/data/now.json"
    sys.exit(main(out_path))
