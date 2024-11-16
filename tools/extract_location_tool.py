from langchain_core.tools import tool
from services.embedding_service import EmbeddingService
from data.locations import fetch_en_locations, fetch_ar_locations

import os


@tool
def extract_location_tool(user_input: str, language: str) -> dict:
    """
    Extracts location information from the user's message.

    Args:
        user_input (str): The user's message.
        language (str): The language of the user's message.

    Returns:
        A dictionary with the location data if a location is found, otherwise None.
    """

    embedding_service = EmbeddingService(api_key=os.getenv("OPENAI_API_KEY"))

    vector_store = embedding_service.generate_locations_embeddings(
        fetch_ar_locations() if language == 'ar' else fetch_en_locations())

    location_data = embedding_service.find_matching_results(
        user_input, vector_store)

    return {"location_data": location_data}
