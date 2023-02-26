# External modules
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

# Internal modules
from db.schemas.User import *
from db.models.User import *
from db.client import db_client
from db.keys.keys import *

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

def search_user(field: str, key) -> User:
    
    try:
        user = user_schema(db_client.users.find_one({field: key}))
        del user["password"]
        return User(**user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found",
                            headers={"WWW-Autenticate": "Bearer"})
    
def search_user_db(field: str, key) -> User_db:
    
    try:
        user = user_schema(db_client.users.find_one({field: key}))
        return User_db(**user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found",
                            headers={"WWW-Autenticate": "Bearer"})

async def auth_user(token: str = Depends(oauth2)) -> User:


    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials",
                         headers={"WWW-Autenticate": "Bearer"}) 

    try:    
        username = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM).get("username")

        if username is None:
            raise exception
        
    except JWTError:
        
        raise exception


    return search_user(username)    


async def current_user(user: User = Depends(auth_user)) -> User:
   
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials",
                            headers={"WWW-Autenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user",
                            headers={"WWW-Autenticate": "Bearer"})

    return user