from load_data import load_data
from fetch_trails import fetch_trail_network, get_hiking_routes
from build_map import build_map

itinerary = load_data()
stops = itinerary["stops"]

trail_network = fetch_trail_network()
hiking_routes = get_hiking_routes(trail_network, stops)

trail_map = build_map(trail_network, stops, hiking_routes)
trail_map.save("output/map.html")