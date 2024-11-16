import os
import requests
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    def __init__(self):
        self.base_url = os.getenv('HOMES_API_BASE_URL')
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
        })

    def get_locations(self, accept_language='en'):
        url = f"{self.base_url}/locations/all"
        headers = {'Accept-Language': accept_language}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']

    def get_filters(self, accept_language='en'):
        url = f"{self.base_url}/filters-details"
        headers = {'Accept-Language': accept_language}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']

    def get_amenities(self, location_id=None, accept_language='en'):
        url = f"{self.base_url}/amenities/all"
        headers = {'Accept-Language': accept_language}
        params = {}
        if location_id:
            params['location_id'] = location_id
        response = self.session.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['data']
