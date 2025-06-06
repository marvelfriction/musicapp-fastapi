from fastapi import HTTPException, Depends, APIRouter
import bcrypt
import jwt
import uuid
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin
from middleware.auth_middleware import auth_middleware
from database import get_db
from sqlalchemy.orm import Session, joinedload
from config import settings

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
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)
    if not is_match:
        raise HTTPException(400, "Incorrect Password!")
    token = jwt.encode({"id": user_db.id}, settings.token_password_key)
    return {"token": token, "user": user_db}

@router.get("/")
def current_user_data(db: Session=Depends(get_db), auth_dict=Depends(auth_middleware)):
    user = db.query(User).filter(User.id == auth_dict["uid"]).options(
        joinedload(User.favourites)
    ).first()
    if not user:
        raise HTTPException(404, "User not found!")
    return user