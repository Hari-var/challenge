from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request # type: ignore
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer #type: ignore
from pydantic import BaseModel# type: ignore
from database.database import db_dependency
from database.model import User

from typing import Annotated
import requests
from json import load
from passlib.context import CryptContext #type: ignore
from jose import jwt #type: ignore
from jose.exceptions import JWTError #type: ignore
from helpers.config import secret_key, algorithm

router = APIRouter(prefix="/auth", tags=["authentication"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')

class Token(BaseModel):
    access_token:str
    token_type:str

def authenticate_user(db, username: str, password: str):
    user= db.query(User).filter((User.username == username) | (User.email == username)).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id: int, role:str, expires_delta: timedelta):
    encode = {'sub': username, 'user_id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, secret_key, algorithm=algorithm)

async def get_current_user(request: Request):
    
    raw_token = request.cookies.get("access_token_fnol")

    if not raw_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # print("Decoded token source:", "Authorization header" if token else "Cookie")
    # print("Raw token:", raw_token)
    try:
        payload = jwt.decode(raw_token, secret_key, algorithms=[algorithm])
        username = payload.get('sub')
        user_id = payload.get('user_id')
        role = payload.get('role')
        if username is None or user_id is None or role is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validete user')
        return {'username': username, 'user_id': user_id, 'role': role }
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validete user')

@router.post("/token")
async def auth(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
    response: Response,
    remember: bool = False
):
    user = authenticate_user(db , form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 🔑 Adjust expiry based on remember
    if remember:
        expires = timedelta(days=30)   # "remember me" = 30 days
    else:
        expires = timedelta(minutes=30)

    token = create_access_token(user.username, user.user_id, user.usertype, expires) #type: ignore

    # 🔒 Set cookie
    if remember:
        response.set_cookie(
            key="access_token_fnol",
            value=token,
            httponly=True,
            secure=False,   # ⚠️ set True in production
            samesite="lax"
        )
    else:
        response.set_cookie(
            key="access_token_fnol",
            value=token,
            httponly=True,
            max_age=1800,
            expires=1800,
            secure=False,   # ⚠️ set True in production
            samesite="lax"
        )

    return {"message": "Logged in successfully"}


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.post("/logout")
async def logout(response: Response):

    response.delete_cookie("access_token_fnol")
    return {"message": "Logged out successfully"}