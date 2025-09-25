from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()  # loads variables from .env into os.environ
api = os.environ["gemini_API"]

vehicle_images_path = Path(os.environ["images_path"])

database_path = Path(os.environ["db_path"]).as_posix()

SQLALCHEMY_DATABASE_URL_LITE = f"sqlite:///{database_path}"

local_pipe = "LOCALDB#BEEA3B89"

SQLALCHEMY_DATABASE_URL_MASTER = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    fr"Server=np:\\.\pipe\{local_pipe}\tsql\query;"
    r"Database=master;"
    r"Trusted_Connection=yes;"
)

SQLALCHEMY_DATABASE_URL_POLICY = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    fr"Server=np:\\.\pipe\{local_pipe}\tsql\query;"
    r"Database=policy;"
    r"Trusted_Connection=yes;"
)

Cloud_db = os.getenv("cloud_db")



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

PROFILE_UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR")) #type: ignore

pc_ack = os.getenv("pcloud_access_key")

pc_sec = os.getenv("pcloud_secret_key")

bucket_name = os.getenv("pcloud_bucket")

sub_dom = os.getenv("pcloud_subdomain")

megamail = os.getenv("mega_email")

megapwd = os.getenv("mega_pwd")

b2appkey = os.getenv("b2_appkey")

b2appid = os.getenv("b2_appkey_id")
