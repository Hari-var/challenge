from fastapi import APIRouter #type: ignore
from pydantic import BaseModel
from AI_ML.agents import verify_vehicle_images, claims_damage_report

router = APIRouter(prefix="/llm", tags=["LLM"])

class VehicleReportRequest(BaseModel):
    front_img: str
    rear_img: str
    left_img: str
    right_img: str
    make: str
    model: str
    type: str
    year: int

@router.get("/extract_vehicle_details")
async def extract_vehicle_details(Vehicle: VehicleReportRequest):
    result = verify_vehicle_images(
        Vehicle.front_img,
        Vehicle.rear_img,
        Vehicle.left_img,
        Vehicle.right_img,
        Vehicle.make,
        Vehicle.model,
        Vehicle.type,
        Vehicle.year
    )
    return {"valid": result[0], "details": result[1]}

@router.get("/claim_validation")
async def claim_validation (damage_descrition: str, requested_amount: float, claimable_amount: float, image_paths: str):
    """
    Validate a claim based on damage description and associated images.

    Args:
        damage_description (str): Description of the damage.
        image_paths (str): Paths to images related to the claim.

    Returns:
        dict: Validation result.
    """
    
    result = claims_damage_report(damage_descrition, requested_amount, claimable_amount, image_paths)
    return result