# Peaks & Paths: Albanian Riviera to the Balkans

An interactive map that visualizes a backpacking route through Albania, Kosovo, and Montenegro. Built around the Peaks of the Balkans trail, the map renders each stop as a clickable marker with trip details and photos, and draws hiking segments using real trail geometry pulled from OpenStreetMap.

![Map Preview](output/map.png)

---

## Features

- Interactive markers color-coded by stop type (camp, hostel, guesthouse, transit)
- Clickable popups with duration, activities, notes, and photos
- Hiking routes drawn over actual OSM trail geometry
- Cross-border trail support spanning Albania, Kosovo, and Montenegro
- Fully self-contained HTML output — no server needed

---

## Tech Stack

- **osmnx** — queries the OpenStreetMap trail network by country
- **networkx** — merges country graphs and computes shortest paths between hiking stops
- **folium** — renders the interactive Leaflet.js map as a standalone HTML file
- **scikit-learn** — required by osmnx for nearest node lookups

---

## Project Structure

```
peaks-and-paths/
├── data/
│   ├── itinerary.json
│   └── photos/
├── output/
│   └── map.html
├── src/
│   ├── load_data.py
│   ├── fetch_trails.py
│   ├── build_map.py
│   └── main.py
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
python main.py
```

Open `output/map.html` in any browser.

---

## Using Your Own Itinerary

1. Edit `data/itinerary.json` with your own stops, coordinates, and dates
2. Set `segment_to_next` to `"hike"` for trail segments and `"bus"`, `"ferry"`, or `"transit"` for everything else
3. Add photos to `data/photos/` and reference them by filename in the `photo` field
4. Update the country names in `fetch_trail_network()` in `fetch_trails.py` to match your route
5. Run `python main.py`

---

## Data Sources

- Trail network: [OpenStreetMap](https://www.openstreetmap.org/) via osmnx
- Itinerary: Peaks of the Balkans route through Albania, Kosovo, and Montenegro
- Map tiles: Leaflet.js / OpenStreetMap contributors
