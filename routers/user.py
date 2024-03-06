from fastapi import APIRouter
from pydantic import BaseModel

router=APIRouter()

class User(BaseModel):
    id: int
    name: str
    url: str
    age: int

new_list= [User(id=1,name="jose",url="www.jose.com",age=30),User(id=2,name="miguwk",url="www.miguel.com",age=22)]
#revisar funcions de orden superior
def buscado_id(id: int):
    seach_id=filter(lambda i : i.id == id, new_list)
    try:
        return list(seach_id)[0]
    except:
        return{"error"}


@router.delete("/user/{user_id}")
async def user(user_id: int):

    found = False

    for index, saved_user in enumerate(new_list):
        if saved_user.id == user_id:
            del new_list[index]
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}

    

@router.put("/user")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(new_list) :
        if saved_user.id == user.id:
            new_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}

    return user
   
@router.get("/user")
async def root():
    return new_list 

@router.get("/userquery")
async def root(id:int):
    return buscado_id(id)

@router.post("/user/",status_code=201)
async def user(user:User):
    if type(buscado_id(user.id))==User:
        return {"error ya existe usuario"}
    return new_list.append(user)

