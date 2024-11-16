import json


def json_to_string(data):
    """
    Recursively formats the API response to escape curly braces for .format()
    """
    # Dumping the JSON structure to a string
    json_string = json.dumps(data, indent=2)

    # Escaping curly braces by doubling them
    escaped_string = json_string.replace('{', '{{').replace('}', '}}')

    return escaped_string
