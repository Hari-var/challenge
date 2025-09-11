from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()  # loads variables from .env into os.environ
api = os.environ["gemini_API"]

vehicle_images_path = Path(os.environ["images_path"])

database_path = Path(os.environ["db_path"]).as_posix()

SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"

origins = [
    "http://localhost:3000"
]

wkhtlm = Path(os.environ["wkhtml_tool_box"])

basic_user = ['user']

privilaged_user = ['agent','admin']

administrator = ['admin']

admin_username = os.getenv("DEFAULT_ADMIN_USERNAME")

admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD") 

secret_key = os.getenv("SECRET_KEY").strip(" ") #type: ignore

algorithm = os.getenv("ALGORITHM").strip(" ") #type: ignore

print(f"Secret Key: {secret_key}, Algorithm: {algorithm}")
