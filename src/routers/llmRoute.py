from fastapi import APIRouter

from AI_ML.agents import verify_vehicle_images

router = APIRouter(prefix="/llm", tags=["LLM"])

@router.get("/extract_vehicle_details")
async def extract_vehicle_details(
                front_img: str,
                rear_img: str,
                left_img: str,
                right_img: str,
                make: str,
                model: str,
                type: str,
                year: int
            ):
    
    result = verify_vehicle_images(front_img, rear_img, left_img, right_img, make, model, type, year)
    return {"valid": result[0], "details": result[1]}