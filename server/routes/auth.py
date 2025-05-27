from fastapi import HTTPException, Depends
import bcrypt
import uuid
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin
from fastapi import APIRouter
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/signup", status_code=201)
def signup_user(user: UserCreate, db: Session=Depends(get_db)):
    # check if user already exists in db
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(400, "User with same email already exists")
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    # add the user to the db
    user_db = User(id=str(uuid.uuid4()), email=user.email, password=hashed_pw, name=user.name)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    return user_db

@router.post("/login")
def login_user(user: UserLogin, db: Session=Depends(get_db)):
    # check if user exists in db
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(400, "User with this email does not exist")
    # check if password matches or not
    passwd_match = bcrypt.checkpw(user.password.encode(), user_db.password)
    if not passwd_match:
        raise HTTPException(400, "Password is incorrect")
    return user_db

# @router.get("/user/{user_id}")