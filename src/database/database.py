from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from fastapi import Depends #type: ignore
from typing import Annotated
from sqlalchemy.orm import Session
import urllib.parse
from helpers.config import SQLALCHEMY_DATABASE_URL_LITE, SQLALCHEMY_DATABASE_URL_MASTER as master_str, SQLALCHEMY_DATABASE_URL_POLICY as policy_str, Cloud_db

# --- Step 1: Connect to master to create 'policy' DB if missing ---

master_url = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(master_str)}"

# engine_master = create_engine(
#     Cloud_db,
#     isolation_level="AUTOCOMMIT",
#     echo=True
# )

# with engine_master.connect() as conn:
#     conn.execute(text("""
#         IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'policy')
#         BEGIN
#             CREATE DATABASE policy
#         END
#     """))

# # --- Step 2: Connect to the actual 'policy' database ---


# policy_url = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(policy_str)}"

# engine = create_engine(
#     Cloud_db,
#     echo=True
# )
engine = create_engine(
    SQLALCHEMY_DATABASE_URL_LITE,
    connect_args={"check_same_thread": False}
)

# --- Step 3: Create session and Base ---
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# --- Step 4: FastAPI dependency ---
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
