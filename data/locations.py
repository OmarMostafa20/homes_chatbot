from api_clients.api_client import APIClient

api_client = APIClient()


def fetch_locations(language='en'):
    locations = api_client.get_locations(accept_language=language)

    texts = []

    for location in locations:
        # Get location name and id
        location_name = location['name']
        location_id = location['id']

        texts.append(f"Region:{location_name}, Region ID: {location_id}")

        # Get sub locations
        for sub_location in location.get('sub_locations', []):
            sub_location_name = sub_location['name']
            sub_location_id = sub_location['id']
            texts.append(f"Area:{sub_location_name}, Area ID: {sub_location_id}")

    return texts


def fetch_sub_locations_by_id(location_id, language='en'):
    sublocation_ids = []
    locations = api_client.get_locations(accept_language=language)
    for location in locations:
        if location['id'] == location_id:
            sublocation_ids = [sub_location['id'] for sub_location in location['sub_locations']]
            break
    return sublocation_ids


def fetch_en_locations():
    return fetch_locations(language='en')


def fetch_ar_locations():
    return fetch_locations(language='ar')
