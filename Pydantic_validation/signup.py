from pydantic import BaseModel

class signupRequest(BaseModel):
    username : str
    email : str
    password : str
    