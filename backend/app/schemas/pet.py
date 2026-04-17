from pydantic import BaseModel


class PetBase(BaseModel):
    name: str
    species: str
    breed: str


class PetCreate(PetBase):
    pass


class PetRead(PetBase):
    id: int
