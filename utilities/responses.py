from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Union, List, Optional, Dict, Any


class Message(BaseModel):
    type: str = Field(description="Type of the message, e.g., 'text'")
    content: str = Field(description="Content of the message")


class Option(BaseModel):
    content: Optional[str] = Field(description="Content of the option")
    id: str = Field(description="ID of the option")
    is_selected: bool = Field(description="Whether the option is selected")


class ReplyResponse(BaseModel):
    messages: List[Message] = Field(description="List of reply messages")
    chat_uuid: str = Field(description="Chat UUID")
    options_type: Optional[str] = Field(description="Type of options, e.g., 'switch' or 'None'")
    options: Optional[List[Option]] = Field(description="List of options")
    is_chat_ended: bool = Field(description="Whether the chat has ended")
    filters: Union[Dict[str, Any], List[Any]] = Field(default_factory=dict, description="Filters as a dict or a list")
    limit: Optional[Any] = Field(description="Limit of the messages")
