from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    pet_id: int
    message: str = Field(min_length=2)


class CitationRead(BaseModel):
    index: int
    chunk_id: str
    title: str
    source: str
