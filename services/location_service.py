import os
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field

from services.embedding_service import EmbeddingService
from data.locations import fetch_ar_locations, fetch_en_locations


class Response(BaseModel):
    type: str = Field(
        description="Type of the location, e.g., 'region'(location) or 'area'(sub-location)")
    id: int = Field(
        description="ID of the 'region'(location) or 'area'(sub-location)")
    name: str = Field(
        description="Name of the 'region'(location) or 'area'(sub-location)")


# System Template
system_prompt_template = """

You are the best real estate helpful assistant extracts only region or area from user input.

Your task is to assist the user by providing information about specific regions or areas match with our data.

- If the user specifies exactly one region or area in their message:
  - Use the `find_region_or_area_tool` to return the exact match from our data, including the name ID and type.
  - Provide the output as a JSON object matching the Response class structure. (e.g. results:[{{"type": "region", "id": 1, "name": "red sea"}}]) only one match.

-If the user specfies multiple regions or areas in their message:
  - Use the `find_region_or_area_tool` to return the exact match from our data, including the name ID and type.
  - Provide the output as a JSON object matching the Response class structure. (e.g. results:[{{"type": "region", "id": 1, "name": "giza"}}, {{"type": "area", "id": 2, "name": "ain elSokhna"}}])

- If the user specfies an region or area this is outside of Egypt:
  - Respond with: outside
  - Do not proceed further.

- If the user specifies an region or area that is not found in our data:
  - Respond with: no_match
  - Do not proceed further.

- If the user does not specify an exact region or area in their message, but instead mentions features or attributes like "apartment with sea view" or if the message is out of scope:
  - Respond with: None
  - Do not proceed further.

**The expected output is a JSON object matching the Response class structure:**


"""

# Prompt Template
prompt_template = """
Input: {input_message}
Output: 
"""


@tool
def find_region_or_area_tool(user_input: str, language: str) -> Response:
    """
    Takes user input message and extracts only region or area from it and returns relevant region or area with its ID and name.

    Args:
        user_input (str): user input message to compare with
        language (str): language of user input message, either ar/en

    Returns:
        A dictionary matching the Response class structure, containing the type of the location, the ID of the region or area and the name of the region or area.
        None: if no matching region or area is found.

    """
    embedding_service = EmbeddingService(api_key=os.getenv("OPENAI_API_KEY"))

    vector_store = embedding_service.generate_locations_embeddings(
        fetch_ar_locations() if language == 'ar' else fetch_en_locations())

    results = embedding_service.find_matching_results(user_input, vector_store)
    return results


class RegionAreatService:
    def __init__(self, api_key):
        self.main_key = api_key

    def process_message(self, input_message):
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt_template),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ])

            llm = ChatOpenAI(model="gpt-4o-mini",
                             openai_api_key=self.main_key, temperature=0.0)
            tools = [find_region_or_area_tool]

            agent = create_tool_calling_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(
                agent=agent, tools=tools, verbose=True)

            input_formatted = prompt_template.format(
                input_message=input_message)

            return agent_executor.invoke({"input": input_formatted})['output']

        except Exception as e:
            return {"error": f"Error in process_message: {e}"}

    def format_response(self, input_message):
        try:
            # Process the message to get the response
            response = self.process_message(input_message)

            print(response)

            if response == "no_match":
                return "no_match"
            elif response == "outside":
                return "outside"
            elif response == "None":
                return None
            else:
                # Extract the part of the response that contains the JSON
                json_part = response.split('{', 1)[1].rsplit('}', 1)[0]

                # Add back the curly braces
                json_string = '{' + json_part + '}'

                # Attempt to parse the string as JSON
                json_data = json.loads(json_string)

                # Return the JSON data
                return json_data

        except Exception as e:
            return {"error": f"Error in format_response: {e}"}
