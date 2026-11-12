"""
Pakistan Earthquake Monitor
Fetches, processes, and displays seismic activity near Pakistan using the USGS API.

"""

__author__ = "Agha Muhammad Roshaan Khan"

from datetime import datetime, timedelta, timezone
import requests

# Base endpoint for USGS Earthquake API
USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Pakistan geographic bounding box
PAKISTAN_BOUNDS = {
    "minlatitude": 23.5,
    "maxlatitude": 37.5,
    "minlongitude": 60.5,
    "maxlongitude": 77.8,
}


def fetch_earthquakes(days=30, min_magnitude=3.0):
    """
    Fetch earthquake records from the USGS API within Pakistan's bounding box.
    """
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    params = {
        "format": "geojson",
        "starttime": start_date.strftime("%Y-%m-%d"),
        "minmagnitude": min_magnitude,
        "minlatitude": PAKISTAN_BOUNDS["minlatitude"],
        "maxlatitude": PAKISTAN_BOUNDS["maxlatitude"],
        "minlongitude": PAKISTAN_BOUNDS["minlongitude"],
        "maxlongitude": PAKISTAN_BOUNDS["maxlongitude"],
    }

    try:
        response = requests.get(USGS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data: {error}")
        return None


def format_timestamp(epoch_millis):
    """Convert millisecond timestamp to readable UTC date string."""
    seconds = epoch_millis / 1000
    date_obj = datetime.fromtimestamp(seconds, tz=timezone.utc)
    return date_obj.strftime("%Y-%m-%d %H:%M:%S UTC")


def display_earthquakes(data):
    """Process and print a formatted summary table of earthquake events."""
    if not data or "features" not in data:
        print("No earthquake data available.")
        return

    features = data["features"]
    total = len(features)

    if total == 0:
        print("No earthquakes matched your search criteria.")
        return

    print("=" * 80)
    print(f"  PAKISTAN REGION SEISMIC REPORT (Total Events Found: {total})")
    print("=" * 80)
    print(f"{'Magnitude':<10} {'Depth (km)':<12} {'Date & Time (UTC)':<24} {'Location'}")
    print("-" * 80)

    magnitudes = []

    for event in features:
        props = event["properties"]
        geom = event["geometry"]

        mag = props.get("mag")
        place = props.get("place", "Unknown Location")
        time_epoch = props.get("time")

        # Depth is the third coordinate in GeoJSON [longitude, latitude, depth]
        depth = geom["coordinates"][2] if geom and "coordinates" in geom else "N/A"
        formatted_time = format_timestamp(time_epoch) if time_epoch else "Unknown"

        if mag is not None:
            magnitudes.append(mag)
            mag_str = f"M {mag:.1f}"
        else:
            mag_str = "N/A"

        depth_str = f"{depth:.1f} km" if isinstance(depth, (int, float)) else str(depth)

        print(f"{mag_str:<10} {depth_str:<12} {formatted_time:<24} {place}")

    print("-" * 80)
    if magnitudes:
        strongest = max(magnitudes)
        average = sum(magnitudes) / len(magnitudes)
        print(f"Summary: Strongest: M {strongest:.1f} | Average Magnitude: M {average:.1f}")
    print("=" * 80)


def main():
    print("--- Pakistan Earthquake Monitor CLI ---")
    try:
        days_input = input("Enter number of past days to monitor (default 30): ").strip()
        days = int(days_input) if days_input else 30

        mag_input = input("Enter minimum magnitude to filter (default 3.5): ").strip()
        min_mag = float(mag_input) if mag_input else 3.5
    except ValueError:
        print("Invalid input. Using default values: 30 days, magnitude 3.5.")
        days = 30
        min_mag = 3.5

    print(f"\nFetching earthquakes (Past {days} days, Min Magnitude: {min_mag})...\n")
    data = fetch_earthquakes(days=days, min_magnitude=min_mag)
    display_earthquakes(data)


if __name__ == "__main__":
    main()
