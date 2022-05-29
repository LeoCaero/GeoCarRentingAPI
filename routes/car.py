from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Body, status, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.db import db
from schemas.car import CarModel

car = APIRouter()

db = db


@car.get("/cars", response_model=List[CarModel], tags=["CARS"])
async def get_all_cars():
    _cars = await db["cars"].find().to_list(None)
    return _cars


@car.get("/cars/{num}", response_model=List[CarModel], tags=["CARS"])
async def get_x_cars(num: int):
    _cars = await db["cars"].find().to_list(num)
    return _cars


@car.post("/cars", response_model=List[CarModel], tags=["CARS"])
async def create_car(car: List[CarModel] = Body(...)):
    _cars = await db["cars"].find().to_list(100)
    _models = []
    for x in car:
        if x.model not in _models:
            _car = jsonable_encoder(x)
            new_car = await db["cars"].insert_one(_car)
            created_car = await db["cars"].find_one({"_id": new_car.inserted_id})
            _models.append(x.model)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


@car.get("/cars/m/{model}", response_model=CarModel, tags=["CARS"])
async def find_car_by_model(model: str):
    _car = await db["cars"].find_one({"model": model})
    return _car


@car.get("/cars/ms/{model}", response_model=List[CarModel], tags=["CARS"])
async def find_car_by_models(model: str):
    _cars = await db["cars"].find({"model": model}).to_list(None)
    return _cars


@car.delete("/cars", response_model=List[CarModel], tags=["CARS"])
async def remove_cars_dupe():
    _cars = await db["cars"].find().to_list(None)
    _models = []
    for x in _cars:
        if x["transmission"] is not None and x["engine_hp"] is not None and x["engine_hp"] is not None:
            if x["model"] in _models:
                _del_car = await db["cars"].delete_one(x)
            else:
                _models.append(x["model"])
        else:
            _del_car = await db["cars"].delete_one(x)
