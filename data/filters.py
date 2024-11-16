from api_clients.api_client import APIClient
from utilities.json_to_string import json_to_string

api_client = APIClient()


def fetch_filters(language='en'):
    filters_data = api_client.get_filters(accept_language=language)
    return filters_data


def fetch_filters_en():
    """
    Fetches the filters for english language and formats them as a string.

    Returns:
        str: A string representation of the filters.
    """
    filters = fetch_filters()

    filters.pop('location_id', None)

    filters.pop('developer_id', None)

    # Simplify options for property_type_id and consideration_id
    for key in ['property_type_id', 'consideration_id']:
        if key in filters:
            options = filters[key].get('options', [])
            # Keep only 'id' and 'name' for each option
            for option in options:
                option_keys = list(option.keys())
                for k in option_keys:
                    if k not in ['id', 'name']:
                        option.pop(k)

    return json_to_string(filters)
