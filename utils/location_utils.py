import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def request_location_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("Share Location", request_location=True))
    return keyboard


async def find_nearest_hospital(lat, lon):
    # Using OpenStreetMap Nominatim for simplicity
    url = f"https://nominatim.openstreetmap.org/search.php?q=hospital&lat={lat}&lon={lon}&format=jsonv2"
    response = requests.get(url)
    data = response.json()

    if data:
        nearest_hospital = data[0]
        hospital_name = nearest_hospital.get("display_name")
        hospital_lat = nearest_hospital.get("lat")
        hospital_lon = nearest_hospital.get("lon")
        return hospital_name, hospital_lat, hospital_lon
    else:
        return None, None, None


def generate_map_link(user_lat, user_lon, hospital_lat, hospital_lon):
    return f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination={hospital_lat},{hospital_lon}"
