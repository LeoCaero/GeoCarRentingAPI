from fastapi import FastAPI
from routes.user import user
from routes.car import car

app = FastAPI()

app.include_router(user)
app.include_router(car)
