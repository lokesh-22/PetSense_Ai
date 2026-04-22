from pydantic import BaseModel, Field


class PetBase(BaseModel):
    name: str = Field(min_length=1)
    species: str = Field(pattern="^(dog|cat)$")
    breed: str = Field(min_length=2)
    age_years: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    notes: str = ""


class PetCreate(PetBase):
    pass


class PetUpdate(PetBase):
    pass


class ActivePetSwitch(BaseModel):
    pet_id: int


class PetRead(PetBase):
    id: int
    owner_id: int
    breed_profile: dict
    created_at: str
