from openai import OpenAI

class LanguageClassificationService:

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def classify_language(self, message):
        system_message = {
            "role": "system",
            "content": """
            - You are a real state classification assistant. Classify the user's message as English 'en', Arabic 'ar', or other language 'unknown' or if the message is doesn't make sense 'None'.
            - Check if the message indicates to lacations in Egypt translated from orginal arabic name to English e.g. 'Maadi' or 'Smouha'.
            """
        }

            
        examples = [
            {"role": "user", "content": "I'm looking for a new house with 3 bedrooms in a quiet neighborhood."},
            {"role": "assistant", "content": "en"},
            {"role": "user", "content": "أنا مهتم بالعقارات التي يمكن أن تعطي عائدًا جيدًا على الاستثمار."},
            {"role": "assistant", "content": "ar"},
            {"role": "user", "content": "Estoy interesado en propiedades que pueden dar un buen retorno de la inversión."},
            {"role": "assistant", "content": "unknown"},
            {"role": "user", "content": "asdkjfhakj"},
            {"role": "assistant", "content": "None"}
        ]

        messages = [system_message] + examples + [{"role": "user", "content": message}]
        response = self.client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.0, max_tokens=10)
        classification = response.choices[0].message.content.strip()
        return classification, response.usage.completion_tokens, response.usage.prompt_tokens