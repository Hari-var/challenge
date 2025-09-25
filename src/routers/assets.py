from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from starlette import status
from database.database import db_dependency
from database.model import Vehicle, Policy
from routers.auth import get_current_user

router = APIRouter(prefix="/insurables", tags=["insurables"])
user_dependency = Annotated[dict, Depends(get_current_user)]

class AssetResponse(BaseModel):
    id: int
    type: str
    policy_number: str

@router.get("/assets", response_model=list[AssetResponse])
async def get_assets(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Join Vehicle and Policy tables to get assets with policy numbers
    assets = db.query(Vehicle, Policy).join(Policy, Vehicle.policy_id == Policy.policy_id).all()
    
    return [
        AssetResponse(
            id=vehicle.vehicle_id,
            type=vehicle.typeofvehicle,
            policy_number=policy.policy_number
        )
        for vehicle, policy in assets
    ]