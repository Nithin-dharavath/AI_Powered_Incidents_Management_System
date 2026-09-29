from pydantic import BaseModel, EmailStr, Field

class signupRequest(BaseModel):
    username : str
    email : EmailStr
    password : str = Field(min_length=8, max_length=72)
    
class loginRequest(BaseModel):
    email : EmailStr
    password : str = Field(min_length=8, max_length=72)