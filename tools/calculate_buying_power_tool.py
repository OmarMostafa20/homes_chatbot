from langchain_core.tools import tool
@tool
def calculate_buying_power_tool(cash_or_mortgage: str, down_payment: float, monthly_disposable_income: float) -> str:
    """
    Estimate the user's buying power based on the provided information.
    
    Args:
    cash_or_mortgage: input string for user choose Cash or Mortgage
    down_payment: input float for Down payment
    monthly_disposable_income: input float for Monthly disposable income
    
    Returns:
    A dictionary with the calculated buying power.

    """
    

    mortgage_factor = 10 if cash_or_mortgage.lower() == 'mortgage' else 5

    estimated_mortgage_capacity = (monthly_disposable_income * 12) * mortgage_factor

    total_buying_power = down_payment + estimated_mortgage_capacity

    return {"Downpayment": f"{down_payment} EGP",
            "Estimated Mortgage Capacity": f"{estimated_mortgage_capacity} EGP/Monthly",
            "Estimated Total Buying Power": f"{total_buying_power} EGP."
            }