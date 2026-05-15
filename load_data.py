import json


def load_data(file_path="data/itinerary.json"):
    with open(file_path, mode="r", encoding="utf-8") as file:
        data = json.loads(file.read())
    return data


def split_by_country(stops):
    countries = {}
    for stop in stops:
        if stop["country"] in countries:
            countries[stop["country"]].append(stop)
        else:
            countries[stop["country"]] = [stop]
    return countries