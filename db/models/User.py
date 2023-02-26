from pydantic import BaseModel

class  User(BaseModel):
    """
    Basic 'User' class used for store temporal information about  
    Web page users.
    """

    id: str | None
    username: str
    email: str
    role: str

class User_db(User):
    """
    Basic 'User_db' class used to manage sensitive information about
    Web page users from backend.
    """

    password: str