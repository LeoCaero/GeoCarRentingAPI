
from pydantic import BaseModel
from typing import Optional

from schemas.car import PyObjectId


class Car(BaseModel):
    id: Optional[int]
    make: Optional[str]
    model: Optional[str]
    generation: Optional[str]
    year_from: Optional[int]
    year_to: Optional[int]
    series: Optional[str]
    body_type: Optional[str]
    number_of_seats: Optional[int]
    length_mm: Optional[int]
    width_mm: Optional[int]
    height_mm: Optional[int]
    number_of_cylinders: Optional[int]
    engine_type: Optional[str]
    engine_hp: Optional[int]
    drive_wheels: Optional[str]
    number_of_gears: Optional[int]
    transmission: Optional[str]
    fuel_tank_capacity_l: Optional[int]
    max_speed_km_per_h: Optional[int]
    fuel_grade: Optional[int]
    car_price: Optional[int]
    car_image: Optional[str]
    car_rating: Optional[float]
