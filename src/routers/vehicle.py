from fastapi import APIRouter, HTTPException # type: ignore
from pydantic import BaseModel
from starlette import status # type: ignore

from database.database import db_dependency
from database.model import Vehicle

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

class VehicleRequest(BaseModel):
    policy_id: int
    typeofvehicle: str
    image_path: str | None = None
    make: str
    model: str
    year_of_purchase: int
    damage_report: str | None = None

    model_config = {
        "from_attributes": True
    }

@router.get("/vehicle_details")
async def read_all_vehicles(db: db_dependency):
    return db.query(Vehicle).all()

@router.get("/vehicle_details/{vehicle_id}")
async def read_vehicle(db: db_dependency, vehicle_id:int):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if vehicle is not None:
        return vehicle
    raise HTTPException(status_code=404, detail="User not found")

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
