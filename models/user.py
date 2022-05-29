from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.car import Car


class User(BaseModel):
    id: Optional[int]
    name: str
    surname: Optional[str]
    userImage: Optional[str]
    rentedCars: Optional[int]
    email: EmailStr
    lastLogin: Optional[str]
    password: str
    username: Optional[str]
    cars: Optional[List[Car]]
