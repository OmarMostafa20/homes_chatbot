from langchain_core.tools import tool
import os

@tool
def classify_language_tool(language: str) -> dict:
    """
    Classifies the language of the user's message as 'en', 'ar', 'another language', or 'something by accident'.
    Returns a dictionary with the language classification.
    """
    return {"language": language}