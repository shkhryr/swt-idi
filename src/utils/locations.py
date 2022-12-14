import json
import random

from utils.messages import (
    EVENTS,
    PLACES,
    CAFE,
)

location_dict = {
    EVENTS: 'event',
    PLACES: 'place',
    CAFE: 'food',
}


def location_message(key):
    name = key['name']
    location = key['location']
    longitude = key['GPS'][1]
    latitude = key['GPS'][0]
    link = key['link']
    message = f"š Name: {name}\nš Location: {location}\n"
    maps_message = f"š Yandex Map: {link}\n"
    return message, maps_message, longitude, latitude


def location_randomizer(location_type):
    location_type = location_dict[location_type]
    with open("utils/package.json", "r", encoding='utf-8') as write_file:
        data = json.load(write_file)
        key = random.choice(list(data[location_type].values()))
        return location_message(key)
