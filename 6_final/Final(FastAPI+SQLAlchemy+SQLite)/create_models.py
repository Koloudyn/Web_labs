from pydantic import BaseModel, Field


class Person(BaseModel):
    surname_name: str = Field(min_length=1)
    e_mail: str = Field(min_length=1)
    login: str = Field(min_length=1)
    password: str = Field(min_length=1)

class Place(BaseModel):
    allow_night: bool = Field()

class PC(BaseModel):
    room_id: int = Field()
    motherboard: str = Field(min_length=1)
    cpu: str = Field(min_length=1)
    ram: str = Field(min_length=1)
    gpu: str = Field()
    power_supply: str = Field(min_length=1)
    drives: str = Field(min_length=1)
    case: str = Field()

