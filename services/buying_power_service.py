from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI

# Example Scenarios
example_scenarios = [
    {"User Input": "I plan to take a mortgage. My current down payment is 200,000 EGP, and my monthly disposable income is 10,000 EGP.",
      "Response": "Down Payment: 200,000 EGP\nEstimated Mortgage Capacity: 1,200,000 EGP\nEstimated Total Buying Power: 1,400,000 EGP"},
]

# Formatted Scenarios
formatted_scenarios = "\n".join(
    [f"**User Input**: \"{scenario['User Input']}\"\n   - **Response**: {scenario['Response']}" for scenario in example_scenarios]
)

# System template
system_prompt_buying_power = """
You are a highly efficient and professional real estate assistant. Your goal is to gather detailed information from the user regarding their buying power. Please follow these steps:

1. Start by greeting the user in a friendly and professional manner.

2.Collect information on the following:

    Whether they plan to purchase with cash or via a mortgage
    The current down payment amount
    Their monthly disposable income

3. Based on the provided information, estimate the user's total buying power.

### Example Scenario:

{formatted_scenarios}

"""

# Prompt Template
prompt_template_buying_power = """
Input: {input_message}
Output: 
"""

@tool
def estimate_buying_power_tool(cash_or_mortgage: str, down_payment: float, monthly_disposable_income: float) -> str:
    """
    Estimate the user's buying power based on the provided information.
    
    Args:
    cash_or_mortgage: input string for user choose Cash or Mortgage
    down_payment: input float for Down payment
    monthly_disposable_income: input float for Monthly disposable income
    """

    mortgage_factor = 10 if cash_or_mortgage.lower() == 'mortgage' else 5

    estimated_mortgage_capacity = (monthly_disposable_income * 12) * mortgage_factor

    total_buying_power = down_payment + estimated_mortgage_capacity

    return f"Down payment: {down_payment} EGP\nEstimated Mortgage Capacity: {estimated_mortgage_capacity} EGP\nEstimated Total Buying Power: {total_buying_power} EGP."


class BuyingPowerService:
    def __init__(self, api_key):
        self.main_key = api_key


    def process_message(self, input_message):
        formatted_system_prompt = system_prompt_buying_power.format(formatted_scenarios=formatted_scenarios)
        prompt = ChatPromptTemplate.from_messages([
            ("system", formatted_system_prompt),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])

        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=self.main_key)
        tools = [estimate_buying_power_tool]

        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        input_formatted = prompt_template_buying_power.format(input_message=input_message)

        return agent_executor.invoke({"input": input_formatted})['output']

