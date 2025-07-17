from fastapi import FastAPI
import database.model as model
from database.database import engine

app = FastAPI()

model.base.metadata.create_all(bind=engine) # type: ignore #ignore