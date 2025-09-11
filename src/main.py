from fastapi import FastAPI   # type: ignore
import database.model as model
from database.database import engine,sessionlocal
from routers import auth, policy, vehicle, user, llmRoute, claims
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from helpers.config import origins
from database.model import User
# import os
from helpers.config import admin_username, admin_password
from passlib.context import CryptContext #type: ignore
from datetime import date

app = FastAPI()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



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


def init_admin():
    db = sessionlocal()
    try:
        # Check if any admin exists
        admin_exists = db.query(User).filter(User.usertype == "admin").first()
        if not admin_exists:
            # Values can come from env vars for security
            default_admin_username = admin_username
            default_admin_password = admin_password 

            admin_user = User(
                usertype="admin",
                username=default_admin_username,
                firstname="System",
                middlename=None,
                lastname="Admin",
                hashed_password=bcrypt_context.hash(default_admin_password), #type: ignore
                dateofbirth=date(2000, 1, 1),  # dummy, update if needed
                phone="0000000000",
                email="admin@example.com",
                address="Default Address"
            )
            db.add(admin_user)
            db.commit()
            print(f"✅ Admin user '{default_admin_username}' initialized")
        else:
            print("ℹ️ Admin already exists, skipping init")
    finally:
        db.close()

# Call admin init at startup
@app.on_event("startup")
def on_startup():
    init_admin()






