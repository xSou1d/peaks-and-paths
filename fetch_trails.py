import osmnx as ox
import networkx as nx

ox.settings.use_cache = True


def fetch_trail_network():
    albania = ox.graph_from_place("Albania", custom_filter='["highway"~"path|track|footway"]')
    kosovo = ox.graph_from_place("Kosovo", custom_filter='["highway"~"path|track|footway"]')
    montenegro = ox.graph_from_place("Montenegro", custom_filter='["highway"~"path|track|footway"]')

    return nx.compose_all([albania, kosovo, montenegro])


def get_hiking_routes(merged_graph, stops):
    routes = []

    for stop_index in range(len(stops) - 1):
        if stops[stop_index]["segment_to_next"] != "hike":
            continue

        start_node = ox.nearest_nodes(merged_graph, stops[stop_index]["lon"], stops[stop_index]["lat"])
        end_node = ox.nearest_nodes(merged_graph, stops[stop_index + 1]["lon"], stops[stop_index + 1]["lat"])

        try:
            path = nx.shortest_path(merged_graph, source=start_node, target=end_node)
            routes.append({
                "start": stops[stop_index]["name"],
                "end": stops[stop_index + 1]["name"],
                "path": path
            })
        except nx.NetworkXNoPath:
            print(f"No path found between {stops[stop_index]['name']} and {stops[stop_index + 1]['name']}")

    return routes