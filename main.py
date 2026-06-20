from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Setup success with venv"}


@app.get("/about")
def get_about():
    return {"message": "This is an about page"}


@app.get("/users")
def get_users(name:str=None):
    return {
        
        "userName" : name
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "userID": user_id
    }

@app.get("/products")
def get_products(productLimit : int = 10):
    return {"Items to be displayed" : productLimit}


@app.get("/items")
def get_items(itemName : str=None, itemPrice:int = 0):
    return {
        "Item Name": itemName,
        "Item Price": itemPrice
    }


# simple post
# @app.post("/create-user")
# def create_user(name:str, age:int):
#     return {
#         "Name" : name,
#         "Age" : age
#     }


# post with dict - but no validation
# @app.post("/create-user")
# def create_user(user:dict):
#     return {
#         "message" : "User created successfully",
#         "data" : user
#     }


# post with pydantic

# class User(BaseModel):
#     name:str
#     age:int

# @app.post("/create-user")
# def create_user(user:User):
#     return {
#         "message" : "User created",
#         "data" : user
#     }


# Nested Model

class Address(BaseModel):
    city : str
    pincode : int

class User(BaseModel):
    name:str
    age:int
    email:str
    address : Address

@app.post("/create-user")
def create_user(user:User):
    return user