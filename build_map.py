import folium
import base64


def encode_photo(photo_path):
    with open(photo_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_map(merged_graph, stops, routes):
    trail_map = folium.Map(location=(41.15, 20.17), zoom_start=8)

    for each_stop in stops:
        if each_stop["photo"]:
            encoded_photo = encode_photo(f"data/photos/{each_stop['photo']}")
            photo_html = f'<img src="data:image/jpeg;base64,{encoded_photo}" width="250"><br>'
        else:
            photo_html = ""

        popup_html = (
            f"{photo_html}<br><br>"
            f"<b>{each_stop['name']}</b><br><br>"
            f"<b>Duration:</b> {each_stop['duration']}<br><br>"
            f"<b>Activities:</b> {', '.join(each_stop['activities'])}<br><br>"
            f"<b>Notes:</b> {each_stop['notes']}"
        )

        if each_stop["type"] == "transit":
            marker_color = "gray"
        elif each_stop["type"] == "camp":
            marker_color = "green"
        elif each_stop["type"] == "hostel":
            marker_color = "blue"
        elif each_stop["type"] == "guesthouse":
            marker_color = "orange"

        folium.Marker(
            location=(each_stop["lat"], each_stop["lon"]),
            icon=folium.Icon(color=marker_color),
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(trail_map)

    for each_route in routes:
        coordinate_list = []

        for each_node in each_route["path"]:
            coordinate_list.append((merged_graph.nodes[each_node]["y"], merged_graph.nodes[each_node]["x"]))

        folium.PolyLine(
            locations=coordinate_list,
            color="green",
            weight=4,
            tooltip=f"{each_route['start']} to {each_route['end']}"
        ).add_to(trail_map)

    return trail_map