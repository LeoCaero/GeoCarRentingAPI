from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


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


class CarModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    make: Optional[str] = Field(...)
    model: Optional[str] = Field(...)
    generation: Optional[str] = Field(...)
    year_from: Optional[int] = Field(...)
    year_to: Optional[int] = Field(...)
    series: Optional[str] = Field(...)
    body_type: Optional[str] = Field(...)
    number_of_seats: Optional[int] = Field(...)
    length_mm: Optional[int] = Field(...)
    width_mm: Optional[int] = Field(...)
    height_mm: Optional[int] = Field(...)
    number_of_cylinders: Optional[int] = Field(...)
    engine_type: Optional[str] = Field(...)
    engine_hp: Optional[int] = Field(...)
    drive_wheels: Optional[str] = Field(...)
    number_of_gears: Optional[int] = Field(...)
    transmission: Optional[str] = Field(...)
    fuel_tank_capacity_l: Optional[int] = Field(...)
    max_speed_km_per_h: Optional[int] = Field(...)
    fuel_grade: Optional[int] = Field(...)
    car_price: Optional[int] = Field(...)
    car_image: Optional[str] = Field(...)
    car_rating: Optional[float] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "make": "AC",
                "model": "ACE",
                "generation": "1 generation",
                "year_from": 1993,
                "year_to": 2000,
                "series": "Cabriolet",
                "body_type": "Cabriolet",
                "number_of_seats": 2,
                "length_mm": 4420,
                "width_mm": 1870,
                "height_mm": 1300,
                "number_of_cylinders": 8,
                "engine_type": "Gasoline",
                "engine_hp": 354,
                "drive_wheels": "Rear wheel drive",
                "number_of_gears": 6,
                "transmission": "Manual",
                "fuel_tank_capacity_l": 90,
                "max_speed_km_per_h": 250,
                "fuel_grade": 95,
                "car_price": 300,
                "car_image": "null",
                "car_rating": 3.5
            }
        }
