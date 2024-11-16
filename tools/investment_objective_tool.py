from langchain_core.tools import tool

@tool
def investment_objective_tool(classification: str) -> dict:
    """
    Classifies the user's investment objective.
    Returns a dictionary with the classification.
    """
    return {"investment_objective": classification}