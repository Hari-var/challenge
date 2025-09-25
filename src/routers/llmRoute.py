import io
from typing import List
from fastapi import APIRouter, UploadFile, File, Depends #type: ignore
from pydantic import BaseModel
from AI_ML.agents import verify_vehicle_images, claims_damage_report

router = APIRouter(prefix="/llm", tags=["LLM"])

class VehicleReportRequest(BaseModel):
    front_img: UploadFile 
    back_img: UploadFile 
    left_img: UploadFile 
    right_img: UploadFile 
    make: str
    model: str
    type: str
    year: int
    
    model_config = {
        "from_attributes": True
    }

@router.post("/extract_vehicle_details")
async def extract_vehicle_details(Vehicle: VehicleReportRequest = Depends()):
    result = verify_vehicle_images(
        Vehicle.front_img,
        Vehicle.back_img,
        Vehicle.left_img,
        Vehicle.right_img,
        Vehicle.make,
        Vehicle.model,
        Vehicle.type,
        Vehicle.year
    )
    return {"valid": result[0], "details": result[1]}

from PIL import Image
@router.post("/claim_validation")
async def claim_validation(
    damage_description: str,
    requested_amount: float,
    claimable_amount: float,
    images: List[UploadFile] = File(...)
):
    """
    Validate a claim based on damage description and associated images.
    """

    pil_images: List[Image.Image] = []

    for file in images:
        contents = await file.read()  # Read file bytes
        pil_images.append(Image.open(io.BytesIO(contents)))  # Convert to PIL Image

    result = claims_damage_report(damage_description, requested_amount, claimable_amount, pil_images)
    return result