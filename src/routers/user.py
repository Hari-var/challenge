from fastapi import APIRouter, HTTPException, Depends, UploadFile, File # type: ignore
from pydantic import BaseModel, EmailStr
from datetime import date
from starlette import status # type: ignore
from typing import Annotated, Optional, Literal, Union

from database.database import db_dependency
from database.model import User
from helpers.config import basic_user, privilaged_user, administrator, PROFILE_UPLOAD_DIR

from passlib.context import CryptContext # type: ignore

from routers.auth import get_current_user
from pathlib import Path
import shutil
import uuid


router = APIRouter(prefix="/users", tags=["users"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserRequest(BaseModel):
    
    username: str
    firstname: str
    middlename: str | None = None
    lastname: str
    password: str
    dateofbirth: date 
    profile_pic: str | None = None
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
    profile_pic: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

class AdminUpdateRequest(UserUpdateRequest):
    usertype: Optional[Literal['user','agent', 'admin']] = None
    status: Optional[Literal['active','inactive']] = None

class Acknowledgement(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    firstname: str
    usertype: str
    middlename: str | None = None
    lastname: str
    hashed_password: str
    dateofbirth: date 
    profile_pic: str | None = None
    phone: str | None = None
    email: str
    address: str | None = None
    status: str

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }
        
# --------------- Applied RBAC -----------------
@router.get("/user_details", response_model= Union[list[UserResponse],UserResponse])
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
            return db.query(User).filter(User.user_id == user.get('user_id')).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"An error occurred: {str(e)}",
        )
    
@router.get("/user_names")
async def get_usernames(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    try:
        role = user.get('role')
        if role in privilaged_user:
            users = db.query(User.user_id, User.username).all()
            usernames = [{ "username":u.username,
                           "user_id":u.user_id} for u in users]  # Extract usernames from tuples
            return usernames
        elif role in basic_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"An error occurred: {str(e)}",
        )
@router.get("/check_username/{username}")
async def get_user_names( username:str, db: db_dependency):
    exists = db.query(User).filter(User.username == username).first()
    return {"exists": exists is not None}  

@router.get("/check_email/{email}")
async def get_user_email( email:str, db: db_dependency):
    exists = db.query(User).filter(User.email == email).first()
    return {"exists": exists is not None} 

@router.get("/check_phone/{phone}")
async def get_user_phone( phone:str, db: db_dependency):
    exists = db.query(User).filter(User.phone == phone).first()
    return {"exists": exists is not None} 

@router.post("/input_user_details", status_code=status.HTTP_201_CREATED)
async def create_user( db: db_dependency, user_request: UserRequest):
    # if user is None:
    #     raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
    #                         detail = "Invalid credentials"
    #     )
    try:
        user_model = User(
            username=user_request.username,
            firstname=user_request.firstname,
            middlename=user_request.middlename,
            lastname=user_request.lastname,
            hashed_password=bcrypt_context.hash(user_request.password),
            dateofbirth=user_request.dateofbirth,
            profile_pic = user_request.profile_pic,
            phone=user_request.phone,
            email=user_request.email,
            address=user_request.address
        )
        # if user.get('role') not in administrator :
        #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
        #                         detail = "You do not have permission to perform this action")
        

        db.add(user_model)
        db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user_details/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency,db: db_dependency, user_id: int):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid Credentials")
    if user.get('role') not in administrator and user.get('user_id') != user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "You do not have permission to perform this action")
    insuree = db.query(User).filter(User.user_id == user_id).first()
    if not insuree:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(insuree)
    db.commit()
    return {"message": "User deleted successfully"}

@router.put("/update_details", status_code=status.HTTP_200_OK)
async def update_user_details(user: user_dependency, db: db_dependency, user_request: UserUpdateRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")
    try:
        role = user.get('role')
        insuree = db.query(User).filter(User.user_id == user.get('user_id')).first()
        if not insuree:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = UserUpdateRequest(**user_request.model_dump(exclude_unset=True))

        for key, value in update_data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(insuree, key, value)

        
        db.commit()
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
         

@router.put("/update_user_details/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user : user_dependency,db: db_dependency, user_id: int, user_request: UserUpdateRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = 'Invalid credentials')
    role = user.get('role')
    if role not in privilaged_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action")
    try:
        insuree = db.query(User).filter(User.user_id == user_id).first()
        if not insuree:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = UserUpdateRequest(**user_request.model_dump(exclude_unset=True))

        for key, value in update_data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(insuree, key, value)

        
        db.commit()
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_user_admin", status_code=status.HTTP_200_OK)
async def update_user_admin(
    user: user_dependency,
    db: db_dependency,
    user_id: int,
    user_request: AdminUpdateRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    role = user.get("role")
    if role not in administrator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    try:
        insuree = db.query(User).filter(User.user_id == user_id).first()
        if not insuree:
            raise HTTPException(status_code=404, detail="User not found")

        # Update only fields that were provided
        update_data = user_request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(insuree, key, value)

        db.commit()
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.post("/upload_pic", status_code=status.HTTP_200_OK )
async def upload_profile_pic(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        file_ext = file.filename.split(".")[-1]
        unique_name = f"{uuid.uuid4()}.{file_ext}"
        file_path = PROFILE_UPLOAD_DIR / unique_name

        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": "Profile picture uploaded successfully", "folder_path": str(PROFILE_UPLOAD_DIR), "file_name": str(unique_name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

from fastapi.responses import FileResponse #type:ignore
@router.get("/get_profile_pic/{user_id}")
def get_profile_pic(user_id: int, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    try:
        insuree = db.query(User).filter(User.user_id == user_id).first()
        
        if not insuree:
            raise HTTPException(status_code=404, detail="User not found")

        if not insuree.profile_pic: # Use direct check for None or empty string #type:ignore
            raise HTTPException(status_code=404, detail="Profile picture not found")

        img_path = Path(PROFILE_UPLOAD_DIR) / insuree.profile_pic

        if not img_path.is_file(): # Check if the file exists on the disk
            raise HTTPException(status_code=404, detail="Profile picture file not found on server")

        return FileResponse(img_path)

    except Exception as e:
        # For security, avoid returning raw exception details in a production environment
        print(f"An unexpected error occurred: {e}") 
        raise HTTPException(status_code=500, detail="An internal server error occurred")

    

@router.get("/user_details/{user_id}")
async def read_user(user: user_dependency, db: db_dependency, user_id: int):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid credentials")
    try:
        if user.get('role') in privilaged_user or user.get('user_id') == user_id:
            user = db.query(User).filter(User.user_id == user_id).first() #type: ignore
            if user:
                return user
            raise HTTPException(status_code=404, detail="User not found")
        
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/acknowledgement", status_code=status.HTTP_201_CREATED)
async def create_acknowledgement(ack_request: Acknowledgement):
    try:
        print(f"""username: {ack_request.username},
                  email: {ack_request.email},
                  password: {ack_request.password}""")
        return {"message": "Acknowledgement created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""

    
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




