from fastapi import APIRouter, Depends # type: ignore
from fastapi.security import OAuth2PasswordRequestForm# type: ignore
from database.database import db_dependency
from database.model import User

from typing import Annotated
import requests
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["authentication"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db, username: str, password: str):
    user= db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

@router.post("/token")
async def auth(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    if not authenticate_user(db , form_data.username, form_data.password):
        return {"error": "Invalid credentials"}
    return db.query(User).filter(User.username==form_data.username).first()