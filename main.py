from fastapi import FastAPI, Depends
from database.models import Users
from sqlalchemy.orm import Session
from database.connection import get_db
from Pydantic_validation.signup import signupRequest

app = FastAPI(   
    title="AI Incidentt powered management system",
    description="web based application used for internal AI powered system",
    version="1.0.0")

@app.get("/health")
async def healthCheck():
    return{
        "status" : "200",
        "version" : "1.0.0",
        "condition" : "working"
    }

@app.post("/register")
async def userRegister(user: signupRequest):
    return{
        "Username" : user.username,
        "Email" : user.email,
        "Password" : user.password
    }

@app.get("/login")
async def userLogin():
    return{"candidate details from db"}


@app.get("/all_users")
def get_users(db : Session = Depends(get_db)):
    usersList = db.query(Users).all()
    if not usersList:
        return{"message" : "user not found in db"}
    return usersList