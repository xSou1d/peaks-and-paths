import folium
import base64
from branca.element import MacroElement
from jinja2 import Template


def encode_photo(photo_path):
    with open(photo_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def add_legend(trail_map):
    legend_html = """
    {% macro html(this, kwargs) %}
    <div style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        z-index: 1000;
        background-color: white;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 13px;
        font-family: Arial, sans-serif;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    ">
        <b>Stop Type</b><br><br>
        <span style="color: gray;">&#9679;</span>&nbsp; Transit<br>
        <span style="color: green;">&#9679;</span>&nbsp; Camp<br>
        <span style="color: blue;">&#9679;</span>&nbsp; Hostel<br>
        <span style="color: orange;">&#9679;</span>&nbsp; Guesthouse<br><br>
        <span style="color: green;">&#9135;&#9135;</span>&nbsp; Hiking Route<br>
        <span style="color: gray;">- - -</span>&nbsp; Transit Route<br>
    </div>
    {% endmacro %}
    """
    macro = MacroElement()
    macro._template = Template(legend_html)
    macro.add_to(trail_map)


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
            f"<b>Notes:</b> {each_stop['notes']}<br><br>"
            f"<details><summary><b>Read more</b></summary><br>{each_stop['description']}</details>"
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

    for stop_index in range(len(stops) - 1):
        locations = [
            (stops[stop_index]["lat"], stops[stop_index]["lon"]),
            (stops[stop_index + 1]["lat"], stops[stop_index + 1]["lon"])
        ]

        if stops[stop_index]["segment_to_next"] != "hike" and stops[stop_index]["segment_to_next"] != None:
            folium.PolyLine(
                locations=locations,
                color="gray",
                weight=2,
                dash_array="5 5",
                tooltip=f"{stops[stop_index]['name']} to {stops[stop_index + 1]['name']}"
            ).add_to(trail_map)

    add_legend(trail_map)
    return trail_map