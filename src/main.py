from fastapi import FastAPI   # type: ignore
import database.model as model
from database.database import engine
from routers import auth, policy, vehicle, user, llmRoute, claims
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from helpers.config import origins

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all (not safe in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

app.include_router(policy.router)

app.include_router(vehicle.router)

app.include_router(claims.router)

app.include_router(llmRoute.router)

app.include_router(auth.router)



model.Base.metadata.create_all(bind=engine) # type: ignore 









