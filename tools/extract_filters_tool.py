from langchain_core.tools import tool
from services.filters_service import FiltersService
import os

@tool
def extract_filters_tool(input_filters: str, language: str, location_id=None) -> dict:
    """
    Extracts filters and preferences from the user's message.
    Returns a dictionary with the filters and options.

    Args:
        input_filters (str): The user's message.
        language (str): The language of the user's message.
        location_id (str, optional): The ID of the location. Defaults to None.

    Returns:
        filters (dict): The extracted filters.
    """
    service = FiltersService(api_key=os.getenv("OPENAI_API_KEY"), language=language, location_id=location_id)
    filters, _, _ = service.extract_filters(input_filters)
    # print(f" filters from service {filters}")
    # options = service.amenities
    return {"filters": filters}
