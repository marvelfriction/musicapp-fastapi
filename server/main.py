from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

DATABASE_URL = "postgresql://postgres:1106@localhost:5432/musicapp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(TEXT, primary_key=True, index=True)
    name = Column(VARCHAR(100))
    email = Column(TEXT, unique=True)
    password = Column(LargeBinary)

@app.post("/signup")
def signup_user(user: UserCreate):
    print(user)
    return {"message": "User created successfully", "user": user}