from fastapi import FastAPI, Query, Path
from enum import Enum
from typing import Annotated, Union

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "HII, This is the root route"}

#Path Parameters
@app.get("/items/{item_id}")
async def get_items_by_if(item_id):  
    return {"item_id": item_id}


class Roles(str, Enum):         #this will create a Roles class with all the possible values of it
    admin = "admin"     
    user = "user"
    moderator = "moderator"

@app.get("/models/{model_name}")
async def get_role(role_name: Roles):
    if role_name is Roles.admin:
        return {"role": "admin"}
    if role_name is Roles.moderator:
        return {"role": "moderator"}
    return {"role": "user"}


#Query Params
#when you declare other func params that are not the part of path patams, they are automatically interpreted as "Qurey" params

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

#params can be declared optional by setting their default to None
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10): #skip and limit are set with default values
    return fake_items_db[skip : skip + limit]



#Request Body
#Client -> API, send the message through req body
#To declare a req body, we use pydantic

# 1. get the BaseModel from pydantic
from pydantic import BaseModel
class Item(BaseModel): #data validation will be performed on the basis of this
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.post("/postItems/")
async def create_item(item: Item):
    return item

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length = 50)]): #here the q is optional but if it is there the max length will be 50.
    results = {"items": [{"items_id": "Foo"}, {"items_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# ... (ellipsis) is used to explicitly declare that the value is required. It will force the client to send the value even if it is null
#You can also recieve a list of values
@app.get("/items/getList/")
async def get_list(q: Annotated[list[str] | None, Query()] = None): #default -> q: Annotated[list[str] | None, Query()] = ["foo", "bar"]
    query_items = {"q": q}
    return query_items






