from fastapi import APIRouter, HTTPException# type: ignore
from pydantic import BaseModel
from starlette import status# type: ignore

from typing import Optional, Literal

from database.database import db_dependency
from database.model import Claims

router = APIRouter(prefix="/claims", tags=["claims"])

class ClaimsRequest(BaseModel):
    policy_id: int
    claim_number: str
    damage_description: str
    damage_percentage: float
    damage_image_path: Optional[str] = None
    dete_of_incident: str
    location_of_incident: Optional[str] = None
    fir_no: Optional[str] = None
    claim_date: Optional[str] = None
    requested_amount: float
    approved_amount: Optional[float] = None
    
    claim_status: Literal["active", "inactive", "expired"]

    model_config = {
            "from_attributes": True
        }

@router.get("/claim_details")
async def read_all_claims(db: db_dependency):
    return db.query(Claims).all()

@router.get("/claim_details/{claim_id}")
async def read_claim(db: db_dependency, claim_id: int):
    claim = db.query(Claims).filter(Claims.claim_id == claim_id).first()
    if claim is not None:
        return claim
    raise HTTPException(status_code=404, detail="Claim not found")

@router.post("/claim_details", status_code=status.HTTP_201_CREATED)
async def create_claim(db: db_dependency, claim_request: ClaimsRequest):
    claim_model = Claims(**claim_request.model_dump())
    db.add(claim_model)
    db.commit()
    return {"message": "Claim created successfully"}

@router.put("/claim_details/{claim_id}", status_code=status.HTTP_200_OK)
async def update_claim(db: db_dependency, claim_id: int, claim_request: ClaimsRequest):
    claim = db.query(Claims).filter(Claims.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    for key, value in claim_request.model_dump().items():
        setattr(claim, key, value)
    
    db.commit()
    return {"message": "Claim updated successfully"}

@router.delete("/claim_details/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_claim(db: db_dependency, claim_id: int):
    claim = db.query(Claims).filter(Claims.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    db.delete(claim)
    db.commit()
    return {"message": "Claim deleted successfully"}

