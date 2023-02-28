from fastapi import FastAPI
from routers import myProfile
from db.models.User import *
from db.client import db_client
from db.schemas.User import user_schema

from passlib.context import CryptContext
crypt = CryptContext(schemes=["bcrypt"])


app = FastAPI()

# Add routers
app.include_router(myProfile.router)


# First line code.
@app.get("/")
async def root():
    return "Main page"

@app.post("/addUser")
async def addUser(newUser: User_db):

    user_dict  = dict(newUser)
    
    user_dict["password"] = crypt.hash(user_dict["password"])
    print(f'Flag: {user_dict["password"]}')
    
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    print('Flag2')
    new_user = user_schema(db_client.users.find_one({"_id": id})) # Nombre de la clave única creada por MongoDB es _id
    
    return User(**new_user)
