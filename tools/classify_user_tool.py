from langchain_core.tools import tool

@tool
def classify_user_tool(classification: str) -> dict:
    """
    Classifies the user as 'Home Buyer', 'Property Investor', or 'Irrelevant'.
    
    Args:
        classification (str): The user's classification.

    Returns:
        A dictionary with the classification.
    """

    return {"persona": classification}
