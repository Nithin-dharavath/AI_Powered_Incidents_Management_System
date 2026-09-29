from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.models import Users
from database.connection import get_db
from Pydantic_validation.signup import signupRequest, loginRequest

app = FastAPI(   
    title="AI Incidentt powered management system",
    description="web based application used for internal AI powered system",
    version="1.0.0"
    )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/health")
async def healthCheck():
    return{
        "status" : "200",
        "version" : "1.0.0",
        "condition" : "working"
    }

@app.post("/register")
async def userRegister(user: signupRequest, db : Session = Depends(get_db)):

    existing_user = db.query(Users).filter(Users.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=404,
            detail="Email already exists in database"
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = Users(
        username = user.username,
        email = user.email,
        password_hash = hashed_password,
        is_active = True
    )
    #add to db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "message" : "user registered successfully",
        "user_id" : new_user.id
    }

@app.post("/login")
async def user_login(user : loginRequest, db : Session = Depends(get_db)):
    verify_user = db.query(Users).filter(Users.email == user.email).first()
    if not verify_user :
        raise HTTPException(
            status_code=401,
            detail="password / email is incorrect"
        )

    correct_password = pwd_context.verify(
        user.password,
        verify_user.password_hash
    )

    return {
        "message": "Login successful",
        "user_id": verify_user.id
    }


@app.get("/all_users")
def get_users(db : Session = Depends(get_db)):
    usersList = db.query(Users).all()
    if not usersList:
        return{"message" : "user not found in db"}
    return usersList