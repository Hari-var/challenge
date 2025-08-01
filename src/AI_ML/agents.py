from google import generativeai as genai
import os
import io
from helpers.config import api
from PIL import Image
from json import loads
from helpers.file_handlers import Load, Extract
from helpers.prompts import vehicle_details_extract_prompt as prompt
import ollama

def gemini_ai(prompt: str, *args : Image.Image):
    genai.configure(api_key = api)
    model = genai.GenerativeModel("gemini-2.5-flash")
    contents = []
    for img in args:
        if isinstance(img, Image.Image):
            contents.append( img)
        else:
            print("Warning: One of the arguments is not a valid PIL Image")

    contents.append({"text": prompt})

    try:

        response = model.generate_content(contents=contents, stream=False)

        return response.text

    except Exception as e:
        print(f"Error during Gemini inference: {e}")
        return None
    
def verify_vehicle_images(front, back, left, right,make,model,type,year):
    front= Image.open(front)  
    back = Image.open(back)
    left = Image.open(left)
    right = Image.open(right)
    ex=Extract()
  # Replace with the appropriate response value
    response = gemini_ai(prompt,front, back, left, right )
    rectify = ex.extract_code(response) 
    result = loads(rectify)
    year_range = list(map(int,result['Manufacturing_year_range'].split('-')))
    year_validity = year_range[0] <= int(year)

    if result['make'].lower() == make.lower() and result['model'].lower() == model.lower() and result['vehicle_type'].lower()==type.lower() and year_validity:
        return [True, result]
    else:
        result = "Vehicle details are not valid!"
        # print("result['make'].lower() == make.lower()", result['make'].lower(), make.lower())
        # print("result['model'].lower() == model.lower()", result['model'].lower(), model.lower())
        # print("result['vehicle_type'].lower() == type.lower()", result['vehicle_type'].lower(), type.lower())
        # print("year_validity", year_validity, year_range, year)
        return [False,result]
    
def claims_damage_report(damage_description: str, requested_amount: float, claimable_amount: float, image_paths: str):
    """
    Validate a claim based on damage description and associated images.

    Args:
        damage_description (str): Description of the damage.
        image_paths (List[str]): Paths to images related to the claim.

    Returns:
        dict: Validation result.
    """
    if not image_paths:
        raise ValueError("At least one image path must be provided")

    images = Image.open(image_paths) 
    ex = Extract()

    from helpers.prompts import claims_damage_report_and_analysis as  claims_report

    prompt = claims_report(damage_description, requested_amount, claimable_amount)

    response = gemini_ai(prompt,images)
    rectify = ex.extract_code(response) 
    result = loads(rectify)
    
    if response:
        return {"valid": True, "details": result}
    else:
        return {"valid": False, "details": "Failed to validate claim."}


from typing import List
from PIL import Image
import ollama

def llava_ai(prompt: str, *image_paths: str):
    if not image_paths:
        raise ValueError("At least one image path must be provided")

    res = ollama.chat(
        model="cogito:8b",
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': list(image_paths)  # pass the image file paths
            }
        ]
    )

    return res['message']['content']
    

if __name__ == "__main__":
    from helpers.prompts import number_plate_extractor3 as npe

    response = llava_ai(npe("gj01ww7381"),r"C:\practice\challenge\data\trail\download1.jpg")

    print(response)
