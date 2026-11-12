# pakistan-earthquake-monitor
A tool to fetch and display recent earthquakes near Pakistan using the USGS API.
# Pakistan Earthquake Monitoring 
# Pakistan Earthquake Monitor

A command-line Python application that fetches live seismic event data from the United States Geological Survey (USGS) Earthquake API, filtering specifically for earthquakes occurring in and around Pakistan.

---

## How It Works

1. **Geographic Bounding Box**: Because tectonic fault lines cross political borders, the script queries the USGS GeoJSON endpoint using a geographic bounding box covering all of Pakistan and adjacent seismic zones (Latitude: `23.5°N` to `37.5°N`, Longitude: `60.5°E` to `77.8°E`).
2. **Unfiltered Magnitude Retrieval**: Fetches every recorded earthquake within the chosen time window—capturing both minor micro-tremors (below M 2.0) and major seismic events—so no regional activity is hidden.
3. **Data Processing**: Parses the raw GeoJSON response, extracts depth (the third coordinate in `[longitude, latitude, depth]`), and converts UNIX epoch millisecond timestamps into human-readable UTC strings.
4. **Summary Analytics**: Automatically calculates total recorded events, strongest magnitude, weakest magnitude, and average magnitude across the queried period.

---

## Features

- **Live API Integration**: Queries the USGS Earthquake API in real time using Python's `requests` library.
- **Simple Time-Range Filter**: Prompts the user for the number of past days to monitor (defaulting to 30 days).
- **Clean Terminal Table**: Displays aligned columns for Magnitude, Depth (km), UTC Timestamp, and Location.
- **Error Handling**: Uses `response.raise_for_status()` and `try/except` blocks to gracefully catch network or HTTP errors.

---

## Prerequisites

- Python 3.8 or higher
- `requests` library

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TSKDynamo/pakistan-earthquake-monitor
   cd pakistan-earthquake-monitor