from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File # type: ignore
from pydantic import BaseModel
from starlette import status# type: ignore

from typing import Annotated, List, Optional, Literal
from datetime import date

from database.database import db_dependency
from database.model import Claims
from helpers.config import basic_user, privilaged_user, administrator
from helpers.file_handlers import Load
from fastapi.responses import FileResponse #type: ignore
from routers.auth import get_current_user
import json

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
    claim_date: Optional[date] = None
    remarks: Optional[str] = None
    approvable_reason: Optional[str] = None
    requested_amount: float
    approvable_amount: Optional[float] = None
    
    claim_status: Literal['in-review', 'accepted', 'rejected']

    model_config = {
            "from_attributes": True
        }
class ClaimsResponse(ClaimsRequest):
    claim_number: str
    claim_id:int
    damage_image_path: Optional[dict] = None       # ✅ parsed dict in response #type:ignore
    documents_path: Optional[dict] = None #type:ignore

    @classmethod
    def from_orm(cls, obj):
        data = obj.__dict__.copy()

        # Convert string -> dict safely
        for field in ["damage_image_path", "documents_path"]:
            raw_value = data.get(field)
            if raw_value:
                try:
                    data[field] = json.loads(raw_value)
                except Exception:
                    data[field] = None
            else:
                data[field] = None

        return super().model_validate(data)

class ClaimUpdateRequest(BaseModel):
    damage_description_user: Optional[str] = None
    severity_level: Optional[Literal["Low", "Moderate", "High", "Critical"]] = None
    damage_percentage: Optional[float] = None
    damage_image_path: Optional[str] = None
    date_of_incident: Optional[date]=None
    location_of_incident: Optional[str] = None
    documents_path: Optional[str] = None
    fir_no: Optional[str] = None
    claim_date: Optional[date] = None
    remarks: Optional[str] = None
    approvable_reason: Optional[str] = None
    requested_amount: Optional[float] = None
    approvable_amount: Optional[float] = None
    claim_status: Optional[Literal['in-review', 'accepted', 'rejected']] = None
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

@router.post("/upload_claim_images")
async def upload_claim_images(folder_name: str,images: List[UploadFile] = File(...)):
    loader = Load()
    res={}
    saved_paths = await loader.save_claim_images(folder_name, *images)
    print(saved_paths)
    for idx, url in enumerate(saved_paths):
        res[str(idx)] = url
    return {
        "message": f"{len(saved_paths)} claim images uploaded successfully",
        "paths": res
    }

@router.post("/upload_documents")
async def upload_documents(folder_name: str, documents: List[UploadFile] = File(...)):
    loader = Load()
    res={}
    saved_paths = await loader.save_documents(folder_name, *documents)
    for idx, url in enumerate(saved_paths):
        res[str(idx)] = url
    return {
        "message": f"{len(saved_paths)} documents uploaded successfully",
        "paths": str(res)
    }
@router.put("/claim_details/{claim_id}", status_code=status.HTTP_200_OK)
async def update_claim(db: db_dependency, claim_id: int, claim_request: ClaimUpdateRequest):
    claim = db.query(Claims).filter(Claims.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    # only update provided fields, skip missing ones
    update_data = claim_request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(claim, key, value)

    db.commit()
    db.refresh(claim)  # ✅ optional: return updated object

    return {"message": "Claim updated successfully", "claim": claim}

@router.delete("/claim_details/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_claim(db: db_dependency, claim_id: int):
    claim = db.query(Claims).filter(Claims.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    db.delete(claim)
    db.commit()
    return {"message": "Claim deleted successfully"}

@router.get("/files")
async def get_damage_images(db: db_dependency, path):
    return FileResponse(Path(path))  



