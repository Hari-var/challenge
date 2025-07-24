import os

api= os.environ["gemini_API"]

vehicle_images_path =r"C:\practice\challenge\data\images"

database_path = "C:/practice/challenge/data/user/policy.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"

print(api)