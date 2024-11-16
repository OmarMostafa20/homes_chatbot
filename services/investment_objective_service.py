from openai import OpenAI

system_message_objective = """
You are the best real estate helpful assistant.

Ask the user about their main investment objective. The options are:
   - Generate passive income through rentals
   - Long-term property appreciation
   - Build a portfolio of multiple properties
   If the user doesn't select one of these options, they can provide a custom objective.
   
Classify the user's message as 'Investment Objective' or 'Irrelevant'. Only respond with one of these two classifications.
"""

class InvestmentObjectiveService:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def classify_investment_objective(self, message):
        system_message = {
            "role": "system",
            "content": system_message_objective
        }

        examples = [
            {"role": "user", "content": "I want long-term property appreciation."},
            {"role": "assistant", "content": "Investment Objective"},
            {"role": "user", "content": "Can you recommend a restaurant nearby?"},
            {"role": "assistant", "content": "Irrelevant"}
        ]
        messages = [system_message] + examples + [{"role": "user", "content": message}]
        
        response = self.client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.0, max_tokens=10)

        classification = response.choices[0].message.content.strip()

        return classification, response.usage.completion_tokens, response.usage.prompt_tokens
