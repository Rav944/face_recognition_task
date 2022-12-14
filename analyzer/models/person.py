from pydantic import BaseModel
from typing import Optional, Dict


class Person(BaseModel):
    name: str
    gender: str
    age: int
    country: str
    face: Optional[Dict]
    photo: bytes

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Tomek",
                "gender": "M",
                "age": 18,
                "country": "Poland"
            }
        }

