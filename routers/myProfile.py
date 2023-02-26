# External modules
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta


# Internal modules
from db.models.User import User, User_db
from db.schemas.Auth_User import *
from db.schemas.User import *
from db.client import db_client
from db.keys.keys import *

# Relocate
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])


router = APIRouter(prefix="/myProfile", 
                   responses={status.HTTP_404_NOT_FOUND: {"message": "User not found"}}, 
                   tags=["My profile"])



@router.get("/")
async def me(user: User = Depends(current_user)):               
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):   
    
    if not (search_user("username", form.username) == User):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect user") 

    user = search_user_db("username", form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = {"sub": user.username, "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}        


@router.post("/sign_up")
async def signUp(form: OAuth2PasswordRequestForm = Depends()):
    
    if type(search_user("username", form.username)) == User:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="username already in use") 
    
    if type(search_user("email", form.email)) == User:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email already in use") 

    id = db_client.users.insert_one(form).inserted_id

    new_user = user_schema(search_user("_id", id)) # Nombre de la clave única creada por MongoDB es _id

    return User(**new_user)