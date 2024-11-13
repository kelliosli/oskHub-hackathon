import requests
from config import GOOGLE_MAPS_API_KEY


def get_nearest_route(destination):
    # Use Google Maps API to get route to the destination
    response = requests.get(
        f"https://maps.googleapis.com/maps/api/directions/json",
        params={"destination": destination, "key": GOOGLE_MAPS_API_KEY},
    )
    return response.json()
