from fastapi import APIRouter, HTTPException, Depends # type: ignore
from pydantic import BaseModel
from starlette import status# type: ignore

from typing import Annotated, Literal, Optional
from database.database import db_dependency
from database.model import Policy
from helpers.config import basic_user, privilaged_user, administrator

from routers.auth import get_current_user

router = APIRouter(prefix="/policies", tags=["policies"])
user_dependency = Annotated[dict, Depends(get_current_user)]

class PolicyRequest(BaseModel):
    policy_number: Optional[str] = None
    policy_holder: Optional[str] = None
    user_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    premium: Optional[str] = None
    total_claimable_amount: Optional[str] = None
    status: Optional[Literal["active", "inactive", "expired"]] = None

    model_config = {
        "from_attributes": True
    }


@router.get("/policy_details")
async def read_all_policies(db: db_dependency):
    return db.query(Policy).all()

@router.get("/policy_details/{policy_id}")
async def read_policy(db: db_dependency, policy_id:int):
    policy = db.query(Policy).filter(Policy.policy_id == policy_id).first()
    if policy is not None:
        return policy
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/policy_details", status_code=status.HTTP_201_CREATED)
async def create_policy(db: db_dependency, policy_request: PolicyRequest):
    policy_model = Policy(**policy_request.model_dump())
    db.add(policy_model)
    db.commit()
    return {"message": "Policy created successfully"}

@router.put("/policy_details/{policy_id}", status_code=status.HTTP_200_OK)
async def update_policy(db: db_dependency, policy_id: int, policy_request: PolicyRequest):
    policy = db.query(Policy).filter(Policy.policy_id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    for key, value in policy_request.model_dump().items():
        if value is not None:
            setattr(policy, key, value)
    
    db.commit()
    return {"message": "Policy updated successfully"}

@router.delete("/policy_details/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(db: db_dependency, policy_id: int):
    policy = db.query(Policy).filter(Policy.policy_id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    db.delete(policy)
    db.commit()
    return {"message": "Policy deleted successfully"}