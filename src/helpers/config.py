from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()  # loads variables from .env into os.environ
api = os.environ["gemini_API"]

vehicle_images_path = Path(os.environ["images_path"])

database_path = Path(os.environ["db_path"]).as_posix()

SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"

wkhtlm = Path(os.environ["wkhtml_tool_box"])
