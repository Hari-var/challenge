from fastapi import FastAPI   # type: ignore
import database.model as model
from database.database import engine
from routers import auth, policy, vehicle, user, llmRoute

app = FastAPI()

model.base.metadata.create_all(bind=engine) # type: ignore 


app.include_router(user.router)

app.include_router(policy.router)

app.include_router(vehicle.router)

app.include_router(llmRoute.router)

app.include_router(auth.router)









