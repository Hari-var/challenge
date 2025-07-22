

from google import generativeai as genai
import os
import io
from helpers.config import api
from PIL import Image

def gemini_ai(front_img: Image.Image, rear_img: Image.Image, left_img: Image.Image, right_img: Image.Image, prompt: str):
    genai.configure(api_key=api)
    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        contents = [
            front_img,
            rear_img,
            left_img,
            right_img,
            prompt  # or {"text": prompt}, depending on the SDK version
        ]

        response = model.generate_content(contents=contents, stream=False)

        return response.text

    except Exception as e:
        print(f"Error during Gemini inference: {e}")
        return None
    
