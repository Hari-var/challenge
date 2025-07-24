from google import generativeai as genai
import os
import io
from helpers.config import api
from PIL import Image
from json import loads
from helpers.file_handlers import Load, Extract
from helpers.prompts import vehicle_details_extract_prompt as prompt

def gemini_ai(prompt: str, *args : Image.Image):
    genai.configure(api_key=api)
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
    verify = ex.extract_code(response)
    # print(verify) 
    result = loads(verify)
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

    
