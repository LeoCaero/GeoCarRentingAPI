from http.client import HTTPException
from typing import List
from fastapi import Body, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from config.db import db
from routes.car import find_car_by_model
from schemas.car import CarModel
from schemas.user import UserModel

user = APIRouter()

db = db


@user.get("/users", response_model=List[UserModel], response_description="List all users", tags=["USERS"])
async def get_all_users():
    _users = await db["users"].find().to_list(1000)
    return _users


@user.get("/users/{email}", response_model=UserModel, tags=["USERS"])
async def get_user_by_email(email: EmailStr):
    _user = await db["users"].find_one({"email": email})
    return _user


@user.get("/users/u/{searchName}", response_model=List[UserModel], tags=["USERS"])
async def find_user_by_name(searchName: str):
    _users = await db["users"].find().to_list(10)
    _user = [x for x in _users if searchName in x['name']]
    return _user


@user.get("/users/c/{searchName}", response_model=UserModel, tags=["USERS"])
async def get_user_cars(searchName: str):
    _user = await db["users"].find_one({"name": searchName})
    # print(_user)
    _user_cars = []
    if _user is not None:
        if _user["cars"] is not None:
            for y in _user["cars"]:
                print(y)
                _user_cars.append(y)
        else:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=f"User {_user} has no cars")
    else:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=f"User {searchName} not found")


@user.post("/users", response_model=UserModel, tags=["USERS"])
async def create_user(user: UserModel = Body(...)):
    _user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(_user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


async def modify_cars_from_user(userEmail: EmailStr, carModel: str, isAdding: bool):
    _user: UserModel= await get_user_by_email(userEmail)
    _car: CarModel = await find_car_by_model(carModel)
    _user_cars = []
    for x in _user["cars"]:
        _user_cars.append(x["model"])
    if _car["model"] not in _user_cars:
        if isAdding:
            _user["cars"].append(_car)
        else:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=f"Model {_car['model']} doesn't exist")
    else:
        if isAdding:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=f"Model {_car['model']} already exists")
        else:
            _user["cars"].remove(_car)

    await db["users"].update_one({"_id": _user["_id"]}, {"$set": {"cars": _user["cars"]}})

    return JSONResponse(status_code=status.HTTP_200_OK, content=_user)


@user.put("/users/{userEmail}/{carModel}", response_model=UserModel, tags=["USERS"])
async def add_car_to_user(userEmail: EmailStr, carModel: str):
    return await modify_cars_from_user(userEmail, carModel, True)


@user.delete("/users/{userEmail}/{carModel}", response_model=UserModel, tags=["USERS"])
async def delete_car_to_user(userEmail: EmailStr, carModel: str):
    return await modify_cars_from_user(userEmail, carModel, False)


@user.get("/users/login/{userEmail}/{userPassword}", response_model=UserModel, tags=["USERS"])
async def login_user(userEmail: EmailStr, userPassword: str):
    _user = await get_user_by_email(userEmail)
    if _user["password"] == userPassword:
        return _user
    else:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content="PASSWORD NOT MATCH")
