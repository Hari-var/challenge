import json
from pathlib import Path
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File # type: ignore
from pydantic import BaseModel
from starlette import status # type: ignore
from helpers.file_handlers import Load
from helpers.config import basic_user, privilaged_user, administrator

from database.database import db_dependency
from database.model import Vehicle

from routers.auth import get_current_user

router = APIRouter(prefix="/vehicles", tags=["vehicles"])
user_dependency = Annotated[dict, Depends(get_current_user)]

class ImageResponse(BaseModel):
    main_path: str
    front_img: str | None = None
    back_img: str | None = None
    left_img: str | None = None
    right_img: str | None = None

class ImageRequest(BaseModel):
    folder_name: str
    typeofvehicle: str
    front_img: UploadFile 
    back_img: UploadFile 
    left_img: UploadFile 
    right_img: UploadFile 

    model_config = {
        "from_attributes": True
    }

class VehicleRequest(BaseModel):
    policy_id: int
    typeofvehicle: str
    image_path: str
    make: str
    model: str
    year_of_purchase: int
    vin: str
    vehicle_no: str
    damage_report: str | None = None

    model_config = {
        "from_attributes": True
    }
class VehicleResponse(VehicleRequest):
    vehicle_id: int

@router.get("/vehicle_details")
async def read_all_vehicles(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user.get("role") in privilaged_user:
        return db.query(Vehicle).all()
    else:
        return db.query(Vehicle).filter(Vehicle.policy_id == user.get("user_id")).all()

@router.get("/vehicle_details/{vehicle_id}")
async def read_vehicle(user: user_dependency, db: db_dependency, vehicle_id:int):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if user.get("role") in privilaged_user or user.get("user_id") == vehicle.policy.user_id:
        return vehicle
    raise HTTPException(status_code=404, detail="Vehicle not found")

@router.post("/vehicle_details", status_code=status.HTTP_201_CREATED)
async def create_vehicle(db: db_dependency, vehicle_request: VehicleRequest):
    vehicle_model = Vehicle(**vehicle_request.model_dump())
    db.add(vehicle_model)
    db.commit()
    return {"message": "Vehicle created successfully"}

@router.put("/vehicle_details/{vehicle_id}", status_code=status.HTTP_200_OK)
async def update_vehicle(db: db_dependency, vehicle_id: int, vehicle_request: VehicleRequest):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    for key, value in vehicle_request.model_dump().items():
        setattr(vehicle, key, value)
    
    db.commit()
    return {"message": "Vehicle updated successfully"}

@router.delete("/vehicle_details/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(db: db_dependency, vehicle_id: int):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}

@router.post("/upload_vehicle_images", status_code=status.HTTP_201_CREATED)
async def upload_vehicle_images(
    imagerequest: ImageRequest = Depends(),
):
    try:
        loader = Load()
        paths = await loader.save_vehicle_images(
            imagerequest.front_img, imagerequest.back_img, imagerequest.left_img, imagerequest.right_img, imagerequest.folder_name, imagerequest.typeofvehicle
        )
        return {"message": "Images uploaded successfully", "paths": str(paths)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

import ast
from fastapi import HTTPException #type:ignore
from fastapi.responses import FileResponse #type:ignore
from pathlib import Path
import json

@router.get("/get_vehicle_image/{idx}/{side}")
async def get_vehicle_image(user: user_dependency, db: db_dependency, idx: int, side: str):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == idx).first()
    if not vehicle or vehicle.image_path in (None, "null", "{}", ""):
        raise HTTPException(status_code=404, detail="No image paths found")

    # Try parsing as JSON, fallback to dict
    try:
        temp = json.loads(vehicle.image_path) #type:ignore
    except json.JSONDecodeError:
        temp = ast.literal_eval(vehicle.image_path) #type:ignore

    if side not in temp or side == "main_folder" or not temp[side]:
        raise HTTPException(status_code=404, detail="Requested image not found")

    return FileResponse(Path(temp[side]))
