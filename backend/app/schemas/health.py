from pydantic import BaseModel, Field


class SymptomRequest(BaseModel):
    pet_id: int
    symptoms: str = Field(min_length=3)
    duration: str = Field(min_length=2)
