import random
from fastapi import FastAPI, Request
from pydantic import BaseModel, PositiveInt, constr, conint
from enum import Enum
from src.auth.routers.base import base_router
from src.auth.routers.user_router import user_router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

booking_app = FastAPI()
templates = Jinja2Templates(directory="templates")
booking_app.mount("/static", StaticFiles(directory="static"), name="static")

booking_app.include_router(base_router)
booking_app.include_router(user_router)

class Gender(str, Enum):
    male = 'male'
    female = 'female'

class Actor(BaseModel):
    actor_id: PositiveInt
    name: constr(max_length=20) = "Name" 
    surname: constr(max_length=20) = "Surname"
    age: conint(ge = 0, le = 100)
    sex: str 

@booking_app.get("/users", response_class=HTMLResponse)
def get_users(request: Request):
    users = [
        {"id": 1, "first_name": "john", "last_name": "Doe", "age": 30, "email": "john@example.com", "photo": "/static/img/users/user1.jpg"},
        {"id": 2, "first_name": "mike", "last_name": "Rice", "age": 11, "email": "mike@example.com", "photo": "/static/img/users/user2.jpg"},
        {"id": 3, "first_name": "kate", "last_name": "Vito", "age": 5, "email": "kate@example.com", "photo": "/static/img/users/user3.jpg"},
        {"id": 4, "first_name": "alex", "last_name": "Di Stefano", "age": 23, "email": "alex@example.com", "photo": "/static/img/users/user4.jpg"},
        {"id": 5, "first_name": "kris", "last_name": "Zoe", "age": 9, "email": "kris@example.com", "photo": "/static/img/users/user5.jpg"},
        {"id": 6, "first_name": "ann", "last_name": "Kro", "age": 14, "email": "ann@example.com", "photo": "/static/img/users/user6.jpg"},
        {"id": 7, "first_name": "axel", "last_name": "Aby", "age": 46, "email": "axel@example.com", "photo": "/static/img/users/user7.jpg"},
        {"id": 8, "first_name": "leo", "last_name": "Dre", "age": 7, "email": "leo@example.com", "photo": "/static/img/users/user8.jpg"},
        {"id": 9, "first_name": "anastasia", "last_name": "Coe", "age": 18, "email": "anastasia@example.com", "photo": "/static/img/users/user9.jpg"},
        {"id": 10, "first_name": "viktor", "last_name": "Boe", "age": 35, "email": "viktor@example.com", "photo": "/static/img/users/user10.jpg"}
    ]

    filtered_users = [user for user in users if 15 < user["age"] < 45]
    valid_users = []
    for user in filtered_users:
        if all(c.isalpha() or c.isspace() for c in user["first_name"] + user["last_name"]):
            valid_users.append(user)
    
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"users": valid_users}
    )


@booking_app.get("/")
def get_five_numbers() -> list:
    return [random.randint(0,100) for i in range(5)]

@booking_app.get("/items/{item_id}/{number}")
def get_path_params(number: int) -> dict:
    return {"number": number}

@booking_app.get("/items")
def get_query_params(name: str, age: int) -> dict:
    return {"name": name,
            "age": age}

@booking_app.get("/items/{name}")
def get_query_path_params(name: str, hieght: int, weight: int) -> dict:
    return {"name": name,
            "hieght": hieght,
            "weight": weight}

@booking_app.post("/actors", response_model=Actor)
def get_actor() -> Actor:
    actor_db = {
        "actor_id": 1,
        "name": "Kianu",
        "surname": "Rivs",
        "age": 53,
        "sex": "male" 
    }
    actor = Actor(**actor_db)
    return actor

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(booking_app, host="0.0.0.0", port=8000)
