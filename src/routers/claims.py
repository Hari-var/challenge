from fastapi import APIRouter, HTTPException, Depends # type: ignore
from pydantic import BaseModel
from starlette import status# type: ignore

from typing import Annotated, Optional, Literal
from datetime import date

from database.database import db_dependency
from database.model import Claims
from helpers.config import basic_user, privilaged_user, administrator

from routers.auth import get_current_user

router = APIRouter(prefix="/claims", tags=["claims"])
user_dependency = Annotated[dict, Depends(get_current_user)]

class ClaimsRequest(BaseModel):
    policy_id: int
    subject_id: int
    # claim_number: str
    damage_description_user: str
    damage_description_llm: str
    severity_level: Literal["Low", "Moderate", "High", "Critical"]
    damage_percentage: float
    damage_image_path: Optional[str] = None
    date_of_incident: date
    location_of_incident: Optional[str] = None
    documents_path: Optional[str] = None
    fir_no: Optional[str] = None
    claim_date: date
    requested_amount: float
    approvable_amount: Optional[float] = None
    
    claim_status: Literal["active", "inactive", "expired"]

    model_config = {
            "from_attributes": True
        }
class ClaimsResponse(ClaimsRequest):
    claim_number: str
    claim_id:int

# ------------------------------------------- RBAC Implemented ------------------------------------------------------
@router.get("/claim_details")
async def read_all_claims(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    role = user.get('role')
    if role in privilaged_user:        
        claims = db.query(Claims).all()
        if not claims:
            raise HTTPException(status_code=404, detail="No claims found")   
        return claims
            
    elif role in basic_user:
        user_id = user.get("user_id")
        claims = db.query(Claims).filter(Claims.policy.has(user_id=user_id)).all()
        if not claims:
            raise HTTPException(status_code=404, detail="No claims found")   
        return claims

# ---------------------------------------------------------------------------------------------------------------
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

