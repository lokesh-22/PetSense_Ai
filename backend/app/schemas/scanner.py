from pydantic import BaseModel, Field


class IngredientScanRequest(BaseModel):
    ingredients_text: str = Field(min_length=3)
