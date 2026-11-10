"""
Pakistan Earthquake Monitor
Fetches recent seismic events near Pakistan using the USGS Earthquake API.
"""

from datetime import datetime
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


def fetch_earthquakes(days: int = 30, min_magnitude: float = 3.0):
    """
    Fetch earthquake records from the USGS API within Pakistan's bounding box.
    """
    params = {
        "format": "geojson",
        "starttime": (
            datetime.utcnow() - requests.compat.timedelta(days=days)
        ).strftime("%Y-%m-%d"),
        "minmagnitude": min_magnitude,
        "minlatitude": PAKISTAN_BOUNDS["minlatitude"],
        "maxlatitude": PAKISTAN_BOUNDS["maxlatitude"],
        "minlongitude": PAKISTAN_BOUNDS["minlongitude"],
        "maxlongitude": PAKISTAN_BOUNDS["maxlongitude"],
    }

    try:
        response = requests.get(USGS_API_URL, params=params, timeout=10)
        # Raise HTTPError if status code is 4xx or 5xx
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data from USGS API: {error}")
        return None


if __name__ == "__main__":
    print("Fetching earthquake data for Pakistan region...")
    data = fetch_earthquakes(days=30, min_magnitude=3.5)

    if data and "features" in data:
        count = data["metadata"]["count"]
        print(f"Total earthquakes found: {count}\n")

        for event in data["features"][:5]:  # Display top 5 events
            props = event["properties"]
            place = props["place"]
            mag = props["mag"]
            print(f"- M {mag:.1f} | {place}")
    else:
        print("No earthquake data retrieved.")
