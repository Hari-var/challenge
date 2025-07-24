from database.database import base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, CheckConstraint
from sqlalchemy.orm import relationship

class User(base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    usertype = Column(String, nullable=False, default='user')
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    middlename = Column(String)
    lastname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    dateofbirth = Column(DateTime, nullable=False)
    phone = Column(String)
    email = Column(String, unique=True, nullable=False)
    address = Column(String)

    policies = relationship("Policy", back_populates="user")

    __table_args__ = (
        CheckConstraint("usertype IN ('user', 'agent', 'admin')", name="user_type_check"),
    )

class Policy(base):
    __tablename__ = "policies"

    policy_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_number = Column(String, unique=True, nullable=False)
    policy_holder = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    premium = Column(Float, nullable=False)
    total_claimable_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="policies")
    vehicles = relationship("Vehicle", back_populates="policy")
    claims = relationship("Claims", back_populates="policy")

    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive', 'expired')", name="policy_status_check"),
    )

class Vehicle(base):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_id = Column(Integer, ForeignKey("policies.policy_id", ondelete="CASCADE"), nullable=False)
    typeofvehicle = Column(String, nullable=False)
    image_path = Column(String)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year_of_purchase = Column(Integer, nullable=False)
    chasis_no = Column(String, nullable=False)
    vehicle_no= Column(String, nullable=False)
    damage_report = Column(String)

    policy = relationship("Policy", back_populates="vehicles")
    claims = relationship("Claims", back_populates="vehicle")

class Claims(base):
    __tablename__ = "claims"

    claim_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_id = Column(Integer, ForeignKey("policies.policy_id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"), nullable=False)
    claim_number = Column(String, unique=True, nullable=False)
    damage_description = Column(String, nullable=False)
    damage_percentage = Column(Float, nullable=False)
    damage_image_path = Column(String)
    date_of_incident = Column(DateTime, nullable=False)
    location_of_incident = Column(String, nullable=False)
    fir_no = Column(String, nullable=True) 
    claim_date = Column(DateTime, nullable=True)
    requested_amount = Column(Float, nullable=False)
    approved_amount = Column(Float, nullable=True)
    claim_status = Column(String, nullable=False)

    policy = relationship("Policy", back_populates="claims")
    vehicle = relationship("Vehicle", back_populates="claims")

    __table_args__ = (
        CheckConstraint("claim_status IN ('active', 'inactive', 'expired')", name="claim_status_check"),
    )