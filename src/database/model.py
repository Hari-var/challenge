from database.database import base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

class User(base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    usertype = Column(String, nullable=False, default='user', check_constraint="usertype IN ('user', 'agent', 'admin')")
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    middlename = Column(String)
    lastname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    dateofbirth = Column(DateTime, nullable=False)
    phone = Column(String)
    email = Column(String, unique=True, nullable=False)
    address = Column(String)
    policies = relationship("Policy", back_populates="user")

class Policy(base):
    __tablename__ = "policies"

    policy_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_number = Column(String, unique=True, nullable=False)
    policy_holder = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    premium = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="policies")
    vehicles = relationship("Vehicle", back_populates="policy")

class Vehicle(base):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_id = Column(Integer, ForeignKey("policies.policy_id"), nullable=False)
    typeofvehicle = Column(String, nullable=False)
    image_path = Column(String)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year_of_purchase = Column(Integer, nullable=False)
    damage_report = Column(String)

    policy = relationship("Policy", back_populates="vehicles")