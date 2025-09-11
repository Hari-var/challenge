from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Depends # type: ignore
from pydantic import BaseModel
from starlette import status# type: ignore

from typing import Annotated, Literal, Optional
from database.database import db_dependency
from database.model import Policy
from helpers.config import basic_user, privilaged_user, administrator

from routers.auth import get_current_user
from json import load
from routers.vehicle import VehicleResponse
from routers.claims import ClaimsResponse
from routers.user import UserResponse

router = APIRouter(prefix="/policies", tags=["policies"])
user_dependency = Annotated[dict, Depends(get_current_user)]

class insurableResponse(BaseModel):
    id: int
    type: str
    policy_id: int
    image_path: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class PolicyListResponse(BaseModel):
    policy_id: int
    policy_number: str
    policy_holder: str
    start_date: date
    end_date: date
    premium: float
    coverage_amount: float
    status: str
    # vehicle_details: list[VehicleRequest] = [] 

    model_config = {
        "from_attributes": True
    }

class PolicyResponse(PolicyListResponse):
    insurable_details: list[insurableResponse] = [] 
    filed_claims: list[ClaimsResponse] = []
    user: UserResponse



class PolicyRequest(BaseModel):
    # policy_number: Optional[str] = None
    # policy_holder: Optional[str] = None
    user_id: int
    start_date: date
    end_date: date
    premium: float
    coverage_amount: float
    status: Literal["active", "inactive", "expired"] 

    model_config = {
        "from_attributes": True
    }

class PolicyUpdateRequest(BaseModel):
    policy_number: Optional[str] = None
    # policy_holder: Optional[str] = None
    user_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    premium: Optional[str] = None
    total_claimable_amount: Optional[str] = None
    status: Optional[Literal["active", "inactive", "expired"]] = None

    model_config = {
        "from_attributes": True
    }


# ----------------------------------------Applied RBAC ----------------------------------------------------
@router.get("/policy_details", response_model = list[PolicyListResponse])
async def read_all_policies(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    try:
        role = user.get('role')
        if role in privilaged_user:
            policies = db.query(Policy).all()
            if not policies:
                raise HTTPException(status_code=404, detail="No policies found")
            return [{
                "policy_id": policy.policy_id,
                "policy_number": policy.policy_number,
                "policy_holder": policy.policy_holder,
                "start_date": policy.start_date,
                "end_date": policy.end_date,
                "premium": policy.premium,
                "coverage_amount": policy.coverage_amount,
                "status": policy.status,
            } for policy in policies]

        elif role in basic_user:
            policies = db.query(Policy).filter(Policy.user_id == user.get('user_id')).all()
            # print(**policies[0].vehicles)
            if not policies:
                raise HTTPException(status_code=404, detail="No policies found")
            return [{
                "policy_id": policy.policy_id,
                "policy_number": policy.policy_number,
                "policy_holder": policy.policy_holder,  # <-- Use the property
                "start_date": policy.start_date,
                "end_date": policy.end_date,
                "premium": policy.premium,
                "coverage_amount": policy.coverage_amount,
                "status": policy.status,
                
            } for policy in policies]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
    
@router.post("/policy_details", status_code=status.HTTP_201_CREATED)
async def create_policy(user: user_dependency,db: db_dependency, policy_request: PolicyRequest):
    if user.get('role') in privilaged_user:
        policy_model = Policy(**policy_request.model_dump())
        # policy_model.user_id = int(user.get("user_id")) #type: ignore
        db.add(policy_model)
        db.commit()
        return {"message": "Policy created successfully"}
    else:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
@router.get("/policy_details/{policy_id}", response_model = PolicyResponse)
async def read_policy(user1: user_dependency, db: db_dependency, policy_id:int):
    if user1 is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    # try:
    policy = db.query(Policy).filter(Policy.policy_id == policy_id).first()
    if policy is not None:
        if user1.get('role') in privilaged_user or policy.user_id == user1.get('user_id'):
            return {
                "policy_id": policy.policy_id,
                "policy_number": policy.policy_number,
                "policy_holder": policy.policy_holder,
                "start_date": policy.start_date,
                "end_date": policy.end_date,
                "premium": policy.premium,
                "coverage_amount": policy.coverage_amount,
                "status": policy.status,
                "insurable_details":  policy.insurables,
                "filed_claims": policy.claims,
                "user": policy.user,
            }
    raise HTTPException(status_code=404, detail="Policy not found")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.delete("/policy_details/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(user: user_dependency, db: db_dependency, policy_id: int):
    policy = db.query(Policy).filter(Policy.policy_id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    if user.get('role') in privilaged_user:
        db.delete(policy)
        db.commit()
        return {"message": "Policy deleted successfully"}
    else:
        raise HTTPException(status_code=403, detail="Operation not permitted")

# ----------------------------------------------------------------------------------------------------------------------





@router.put("/policy_details/{policy_id}", status_code=status.HTTP_200_OK)
async def update_policy(db: db_dependency, policy_id: int, policy_request: PolicyUpdateRequest):
    policy = db.query(Policy).filter(Policy.policy_id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    for key, value in policy_request.model_dump().items():
        if value is not None:
            setattr(policy, key, value)
    
    db.commit()
    return {"message": "Policy updated successfully"}

