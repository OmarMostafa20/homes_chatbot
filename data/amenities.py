from api_clients.api_client import APIClient

api_client = APIClient()


def fetch_amenities(location_id, language='en'):
    amenities = api_client.get_amenities(
        location_id=location_id, accept_language=language)
    # Extract only id and name
    simplified_amenities = [{"id": amenity["id"], "name": amenity["name"]} for amenity in amenities]
    return simplified_amenities
