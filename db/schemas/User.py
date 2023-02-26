def user_schema(user) -> dict:
    """
    Function used to create a JSON object from "User" object
    """

    return {"id": str(user["_id"]), "username": user["username"], "email": user["email"]}

def users_schema(users) -> list:
    """
    Function used to create a list of JSON objects from "User" objects
    """
    
    return [user_schema(user) for user in users] 