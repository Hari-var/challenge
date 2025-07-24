from fastapi import APIRouter, HTTPException# type: ignore
from pydantic import BaseModel
from starlette import status# type: ignore

from typing import Literal
from database.database import db_dependency
from database.model import Policy

router = APIRouter(prefix="/policies", tags=["policies"])

class PolicyRequest(BaseModel):
    policy_number: str
    policy_holder: str
    user_id: int
    start_date: str
    end_date: str
    premium: float
    status: Literal["active", "inactive", "expired"]

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