import os
import json
import time

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.models import ChatMessage
from tools import tools

# Function to retrieve the conversation history
def get_conversation_history(chat_uuid):
    """Retrieve the conversation history for the given chat UUID."""
    messages = ChatMessage.query.filter_by(
        chat_uuid=chat_uuid).order_by(ChatMessage.timestamp.asc()).all()
    history = []
    for msg in messages:
        # Determine whether the message is from the assistant or the user based on the is_bot flag
        prefix = "Assistant:" if msg.is_bot else "User:"
        history.append(f"{prefix} {msg.message}")
    return history


# Create the system prompt
system_prompt = """
You are an efficient and professional real estate assistant. Your goal is to guide users towards finding the best real estate recommendations based on their needs, all while collecting relevant information for optimal filtering and recommendations.

### Steps Instructions:
1. **Language Detection:**
   - Classifies the language of the user's message as English 'en', Arabic 'ar', 'another language', or 'something by accident'.
   - If a language other than English or Arabic is detected, kindly inform the user that only these two languages are supported and ask them to continue in either English or Arabic.

2. **User Classification:**
   - Start by determining whether the user is a **Home Buyer** or a **Property Investor** based on their input message using the classify_user_tool.
   - If the user's input is irrelevant to real estate, politely inform them and encourage them to provide real estate-related information to proceed.
   - Keep the conversation professional and helpful.

3- **Location Extraction:**
    - Extract the location mentioned in the user's input, identifying whether it is an area or a region. Use the extract_location_tool to determine this.
    - If the location is a region, ask the user to specify which area they are interested in in this region based on the available areas I will provide.
    - If the location is not relevant to the ones returning from the extract_location_tool, politely inform the user and ask them to provide a valid location within the supported regions or areas.
    - If the user not mentioned a specific location in the message, politely inform them to provide a location.

4. If user classified as **Home Buyer:** do the following step:
   1- **Gathering Preferences & Filters:**
      - Extract the user's preferences using the extract_filters_tool with lcoation_id extracted from the previous messages.
      - Keep the conversation focused and gradually ask relevant questions to build the user's preferences until all necessary filters are gathered.

5. If user classified as **Property Investor:** do the following two steps:
   1- **Investment Objectives**
      - Ask about their investment objectives (e.g., buy-to-rent, capital growth, etc.) using the investment_objective_tool.
      - Classify the user entered an message as 'Investment Objective' or 'Irrelevant'.
      - If the user's message is 'Irrelevant', politely inform them and encourage them to provide investment objectives to proceed.

   2- **Calculate Buying Power:**
      - Ask the user if currently knowing the buying power or need to calculate it.
      - If the user wants to calculate the buying power, Use the calculate_buying_power_tool to assess the user's financial capacity based on:
      - If planning to finance the investment with a "Mortgage" or using "Cash".
      - If currently have the Downpayment, if yes, ask the user how much.
      - Ask the user about the monthly disposable income.

### Seamless Interaction:
1. After classify the user persona: Make sure After gathering one or more pieces of additional information (beyond persona) (e.g., location, filters, buying power), Return the following option:
    - "{{"options": [{{"content": "Show recommendations", "id": 1, "is_selected": false}}], "option_type": "switch"}}"

2. Always be professional, ensuring that responses are helpful, concise, and tailored to the user's preferences and filters.

### Generic Instructions:
1. The only currency allowed is EGP, if the user enters anything else skip any step, inform them and ask them to enter EGP only.

### Output Instructions:
1. **JSON Response Format:**
   - Always return the response in a structured JSON format, like this:
   {{
      "agent_scratchpad": "Your thoughts for each step before you take actions",
      "messages": [
          {{"type": "area" or "region", "content": "ID of the area or region"}} (if available, if not then don't include it),
          {{"type": "text", "content": "Message content"}}
      ],
      "options" (if available): [
          {{"content": "Option 1", "id": 1, "is_selected": false}},
          {{"content": "Option 2", "id": 2, "is_selected": false}}
      ],
      "options_type": "switch" or "Null" if no options available,
      "is_chat_ended": false unless the conversation is ended,
      "filters": {{
          "location_id": "ID of the area or region if available, if not then don't include it",
          "persona": "home-buyer or investor",
          "buying_power": "total buying power calculated if available, if not then don't include it",
          ** remain the rest of the filters collected through the conversation **
      }}
   }}
"""


input_schema = """Answer the following question asked by one of our users. I will provide you with the user's message and the context of the chat history.

Chat History Context enclosed by ========:
========Chat History Start========
{chat_history}
========Chat History End========

Think before you reply and revise your answer.
Focus on the user's current message and provide a helpful response in the same language and dialect.

Customer's Current Message: {input}"""


llm = AzureChatOpenAI(model="gpt-4o-mini",
                      api_key=os.environ.get('AZURE_OPENAI_API_KEY'),
                      api_version=os.environ.get('OPENAI_API_VERSION'),
                      azure_endpoint=os.environ.get('AZURE_OPENAI_BASE'),
                      temperature=0.0)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)


agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def process_agent(chat_uuid, user_input):
    # Get conversation history
    conversation_history = get_conversation_history(chat_uuid)
    chat_history = "\n".join(conversation_history)

    # Format the input using the input schema
    formatted_input = input_schema.format(
        chat_history=chat_history, input=user_input)

    # Invoke the agent
    try:
        t1 = time.time()
        response = agent_executor.invoke({
            "input": formatted_input,
        })['output']
        t2 = time.time()
        print(f"Response time: {t2 - t1:.2f} seconds")

        json_part = response.split('{', 1)[1].rsplit('}', 1)[0]
        json_string = '{' + json_part + '}'
        json_response = json.loads(json_string)

        # Parse the agent's response and return it
        return json_response

    except Exception as e:
        # Log the error and handle failure case
        print(f"Error invoking agent: {e}")
        return {
            "message": [{"type": "text", "content": "Sorry, something went wrong. Please try again later."}],
            "options": [],
            "is_chat_ended": False,
            "filters": {}
        }



# If the location mentioned is region, return all areas related to that region in filters (e.g., {{filters: {{"location_id": [id of area 1, id of area 2, ...]}}}}) then ask the user to specify which area they are interested in.
