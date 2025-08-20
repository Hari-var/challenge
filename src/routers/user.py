from fastapi import APIRouter, HTTPException, Depends # type: ignore
from pydantic import BaseModel, EmailStr
from datetime import date
from starlette import status # type: ignore
from typing import Annotated, Optional, Literal

from database.database import db_dependency
from database.model import User
from helpers.config import basic_user, privilaged_user, administrator

from passlib.context import CryptContext # type: ignore

from routers.auth import get_current_user


router = APIRouter(prefix="/users", tags=["users"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_dependency = Annotated[dict, Depends(get_current_user)]

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
    # usertype: Optional[str] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    middlename: Optional[str] = None
    lastname: Optional[str] = None
    dateofbirth: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

class AdminUpdateRequest(UserUpdateRequest):
    usertype: Optional[Literal['user','agent', 'admin']]

        
# --------------- Applied RBAC -----------------
@router.get("/user_details")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    try:
        role = user.get('role')
        if role in privilaged_user:
            return db.query(User).all()
        elif role in basic_user:
            return db.query(User).filter(User.user_id == user.get('user_id')).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
    
@router.post("/input_user_details", status_code=status.HTTP_201_CREATED)
async def create_user(user: user_dependency, db: db_dependency, user_request: UserRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid credentials"
        )
    if user.get('role') not in administrator:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "You do not have permission to perform this action")
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

@router.delete("/user_details/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency,db: db_dependency, user_id: int):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid Credentials")
    if user.get('role') not in administrator:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "You do not have permission to perform this action")
    insuree = db.query(User).filter(User.user_id == user_id).first()
    if not insuree:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(insuree)
    db.commit()
    return {"message": "User deleted successfully"}

@router.put("/user_details/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user : user_dependency,db: db_dependency, user_id: int, user_request: UserUpdateRequest | AdminUpdateRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = 'Invalid credentials')
    role = user.get('role')
    if role not in privilaged_user and role not in administrator:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action")
    try:
        insuree = db.query(User).filter(User.user_id == user_id).first()
        if not insuree:
            raise HTTPException(status_code=404, detail="User not found")
        
        if role not in administrator and getattr(user_request, "usertype", None) is not None:
            raise HTTPException(status_code=403, detail="You do not have permission to update usertype")
        
        if role in administrator:
            update_data = AdminUpdateRequest(**user_request.model_dump(exclude_unset=True))
        else:
            update_data = UserUpdateRequest(**user_request.model_dump(exclude_unset=True))

        for key, value in update_data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(insuree, key, value)

        
        db.commit()
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
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
    """




