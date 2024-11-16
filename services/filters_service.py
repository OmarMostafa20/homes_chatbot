from openai import OpenAI

from pydantic import BaseModel, Field
from data.filters import fetch_filters_en
from data.amenities import fetch_amenities
from utilities.json_to_string import json_to_string


class Response(BaseModel):
    amenity_id: list[str] = Field(description="List of IDs of the amenities")
    property_type_id: list[str] = Field(description="List of IDs of the property types")
    consideration_id: list[str] = Field(description="List of IDs of the considerations")
    min_area: int = Field(description="Minimum area of the property")
    max_area: int = Field(description="Maximum area of the property")
    min_price: float = Field(description="Minimum price of the property")
    max_price: float = Field(description="Maximum price of the property")
    finishing_type: str = Field(description="Finishing type of the property")
    bedrooms: int = Field(description="Number of bedrooms")
    bathrooms: int = Field(description="Number of bathrooms")


# System Template
system_prompt_template = """

You are the best real estate helpful assistant.

The user enters some options needed in the vacation home property in the message. Match entered options to the list of our filters and amenities.

List of filters with their definitions:
{filters}

List of amenities with their definitions:
{amenities}
"""


class FiltersService:
    def __init__(self, api_key, language='en', location_id=None):
        self.client = OpenAI(api_key=api_key)
        self.language = language
        self.location_id = location_id
        self.filters = fetch_filters_en()
        self.amenities = ''
        if self.location_id:
            self.amenities = fetch_amenities(
                location_id=self.location_id, language=self.language)
            self.formated_amenities = json_to_string(self.amenities)

    def extract_filters(self, message):
        prompt_template = system_prompt_template.format(
            filters=self.filters, amenities=self.formated_amenities)
        system_message = {
            "role": "system",
            "content": prompt_template
        }

        messages = [system_message] + [{"role": "user", "content": message}]
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.0,
            response_format=Response
        )

        filters = response.choices[0].message.parsed.__dict__
        non_empty_filters = {k: v for k,
                             v in filters.items() if v not in ([], '', 0, 0.0)}

        return non_empty_filters, response.usage.completion_tokens, response.usage.prompt_tokens
