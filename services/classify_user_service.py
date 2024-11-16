from openai import OpenAI


system_prompt = """
1. Home Buyer:

- If the user expresses interest in buying a home for personal use.
- Example phrases:
    "I’m looking for a house to move into."
    "I want to buy a place to live with my family."
    "I'm relocating and need a new home."

2. Property Investor:
- If the user is looking to invest in real estate for profit or rental income.
- Example phrases:
    "I'm interested in investing in real estate."
    "I'm looking for properties to rent out."
    "I want to buy real estate as an investment."

3. Irrelevant:
- If the message does not relate to buying or investing in real estate.
- Example phrases:
    "What’s the weather like today?"
    "I’m interested in stock trading."
    "I need advice on starting a business."
"""
class UserClassificationService:

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def classify_user(self, message):
        system_message = {
            "role": "system",
            "content": system_prompt
        }

        examples = [
            {"role": "user", "content": "Home Buyer"},
            {"role": "assistant", "content": "Home Buyer"},
            {"role": "user", "content": "مشتري منزل"},
            {"role": "assistant", "content": "Home Buyer"},
            {"role": "user", "content": "I'm looking for a new house with 3 bedrooms in a quiet neighborhood."},
            {"role": "assistant", "content": "Home Buyer"},
            {"role": "user", "content": "Property Investor"},
            {"role": "assistant", "content": "Property Investor"},
            {"role": "user", "content": "مستثمر عقاري"},
            {"role": "assistant", "content": "Property Investor"},
            {"role": "user", "content": "I'm interested in properties that can give a good return on investment."},
            {"role": "assistant", "content": "Property Investor"},
            {"role": "user", "content": "Can you recommend a good restaurant nearby?"},
            {"role": "assistant", "content": "Irrelevant"}
        ]

        messages = [system_message] + examples + [{"role": "user", "content": message}]
        response = self.client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.0, max_tokens=10)
        classification = response.choices[0].message.content.strip()
        return classification, response.usage.completion_tokens, response.usage.prompt_tokens