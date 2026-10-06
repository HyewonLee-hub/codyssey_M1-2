from typing import Literal

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ConversationCreate(BaseModel):
    title: str = "새 대화"
    messages: list[ConversationMessage] = Field(
        default_factory=list
    )