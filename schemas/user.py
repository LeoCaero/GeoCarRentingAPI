from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from models.car import Car


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    surname: Optional[str] = Field(...)
    userImage: Optional[str] = Field(...)
    rentedCars: Optional[int] = Field(...)
    email: EmailStr = Field(...)
    lastLogin: Optional[str] = Field(...)
    password: str = Field(...)
    username: Optional[str] = Field(...)
    cars: Optional[List[Car]] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Leo2",
                "surname": "Caero",
                "userImage": "a",
                "rentedCars": 1,
                "email": "leo@gmail.com",
                "lastLogin": "3.0",
                "password": "3.0",
                "username": "rockyrocky",
                "cars": []}
        }
