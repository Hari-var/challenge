from fastapi import APIRouter, HTTPException, Depends, UploadFile, File # type: ignore
from pydantic import BaseModel
from datetime import date
from starlette import status # type: ignore
from typing import Annotated, Optional, Literal, Union
from database.model import Insurable
from routers.auth import get_current_user
from database.database import db_dependency
from helpers.config import basic_user, privilaged_user, administrator


router = APIRouter(prefix="/insurables", tags=["insurables"])
user_dependency = Annotated[dict, Depends(get_current_user)]
class InsurableResponse(BaseModel):
    id: int
    type: str
    policy_number: str
    policy_id: int

    model_config = {
        "from_attributes": True
    }
@router.get("/get_id")
async def get_asset_id(user: user_dependency, db:db_dependency, policy_id: int):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    asset_ids_query = db.query(Insurable.id).filter(Insurable.policy_id == policy_id).all()
    # Convert list of tuples [(1,), (2,)] to [1, 2]
    asset_ids = [aid[0] for aid in asset_ids_query]
    if asset_ids == []:
        raise HTTPException(status_code=404, detail="No assets found")
    return asset_ids

@router.get("/assets", response_model=list[InsurableResponse])
async def read_assets(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Privileged users: see all assets
    if user.get("role") in privilaged_user:
        assets = db.query(Insurable).all()
    else:
        # Basic user: see only their own assets
        assets = (
            db.query(Insurable)
            .filter(Insurable.policy.has(user_id=user.get("user_id")))
            .all()
        )

    if not assets:
        raise HTTPException(status_code=404, detail="No assets found")

    # Convert to response list
    return [{
            "id": a.id,
            "type": a.type,
            "policy_number": a.policy.policy_number,
            "policy_id":a.policy_id,
        }
        for a in assets
    ]