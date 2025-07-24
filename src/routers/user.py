from fastapi import APIRouter, HTTPException # type: ignore
from pydantic import BaseModel, EmailStr
from datetime import date
from starlette import status # type: ignore
from typing import Optional, Literal

from database.database import db_dependency
from database.model import User

from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["users"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRequest(BaseModel):
    
    username: str
    firstname: str
    middlename: str | None = None
    lastname: str
    password: str
    dateofbirth: date | None = None
    phone: str | None = None
    email: str
    address: str | None = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

class UserUpdateRequest(BaseModel):
    usertype: Optional[str] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    middlename: Optional[str] = None
    lastname: Optional[str] = None
    hashed_password: Optional[str] = None
    dateofbirth: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }
        

@router.get("/user_details")
async def read_all(db : db_dependency):
    return db.query(User).all()

@router.get("/user_details/{user_id}")
async def read_user(db : db_dependency, user_id: int):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/user_details/{username}")
async def read_user_by_username(db: db_dependency, username :str):
    user =  db.query(User).filter(User.username==username).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/user_details/policy/{user_id}")
async def read_user_policies(db: db_dependency, user_id: int):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        policies = user.policies  # Assuming User model has a relationship with Policy
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/user_details", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    user_model = User(
        username=user_request.username,
        firstname=user_request.firstname,
        middlename=user_request.middlename,
        lastname=user_request.lastname,
        hashed_password=bcrypt_context.hash(user_request.password),
        dateofbirth=user_request.dateofbirth,
        phone=user_request.phone,
        email=user_request.email,
        address=user_request.address
    )

    db.add(user_model)
    db.commit()
    return {"message": "User created successfully"}

@router.put("/user_details/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(db: db_dependency, user_id: int, user_request: UserUpdateRequest):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_request.model_dump().items():
        setattr(user, key, value)
    
    db.commit()
    return {"message": "User updated successfully"}

@router.delete("/user_details/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: db_dependency, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return user