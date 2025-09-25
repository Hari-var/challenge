from datetime import datetime
from typing import Dict
from database.database import Base
from sqlalchemy import ARRAY, JSON, Column, Integer, String, Date, ForeignKey, Float, CheckConstraint, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    usertype = Column(String(15), nullable=False, default='user')
    username = Column(String(20), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    middlename = Column(String(50))
    lastname = Column(String(50), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    dateofbirth = Column(Date, nullable=False)
    phone = Column(String(15), unique=True, nullable=True)
    email = Column(String(155), unique=True, nullable=False)
    profile_pic = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default='active')
    address = Column(String(400), nullable=True)

    policies = relationship("Policy", back_populates="user")

    __table_args__ = (
        CheckConstraint("usertype IN ('user', 'agent', 'admin')", name="user_type_check"),
        CheckConstraint("status IN ('active', 'inactive')", name="user_status_check"),
    )
    @property
    def dob_str(self):
        if self.dateofbirth is not None:
            return self.dateofbirth.strftime("%Y-%m-%d")
        return None

from sqlalchemy import event, select, func



class Policy(Base):
    __tablename__ = "policies"

    policy_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_number = Column(String(50), unique=True, nullable=False)
    # policy_holder = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    premium = Column(Float, nullable=False)
    coverage_amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default = 'under-review')

    user = relationship("User", back_populates="policies")
    insurables = relationship("Insurable", back_populates="policy", cascade="all, delete")
    claims = relationship(
        "Claims",
        back_populates="policy",
        cascade="all, delete-orphan"   # same for claims
    )

    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive', 'expired', 'under-review')", name="policy_status_check"),
    )
    @property
    def policy_holder(self):
        # Safely handle missing middle name
        parts = [self.user.firstname, self.user.middlename, self.user.lastname]
        return " ".join(filter(None, parts))

@event.listens_for(Policy, "before_insert")
def generate_policy_number(mapper, connection, target):
    today_str = datetime.now().strftime("%Y%m%d")

    # Count policies created today efficiently
    result = connection.execute(
        select(func.count()).where(Policy.policy_number.like(f"POL-{today_str}%"))
    )
    count_today = result.scalar_one()

    target.policy_number = f"POL-{today_str}{count_today + 1:03d}"

class Insurable(Base):
    __tablename__ = "insurable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20), nullable=False)  # e.g., 'vehicle', 'health', 'property'
    policy_id = Column(Integer, ForeignKey("policies.policy_id", ondelete="CASCADE"), nullable=False)

    

    policy = relationship("Policy", back_populates="insurables")
    claims = relationship("Claims", back_populates="subject")

    __mapper_args__ = {
        "polymorphic_identity": "insurable",
        "polymorphic_on": type
    }

class Vehicle(Insurable):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer, ForeignKey("insurable.id", ondelete="CASCADE"), primary_key=True)
    typeofvehicle = Column(String(20), nullable=False)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year_of_purchase = Column(Integer, nullable=False)
    vin = Column(String(100), nullable=False, unique=True)
    image_path = Column(String(500), nullable=True)  # Changed to JSON type
    vehicle_no = Column(String(100), nullable=False)
    damage_report = Column(String(3000))

    __mapper_args__ = {
        "polymorphic_identity": "vehicle"
    }



class Claims(Base):
    __tablename__ = "claims"

    claim_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_id = Column(Integer, ForeignKey("policies.policy_id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("insurable.id"), nullable=False)
    claim_number = Column(String(50), unique=True, nullable=False)
    damage_description_user = Column(String(3000), nullable=False)
    damage_description_llm = Column(String(3000), nullable=False)
    severity_level = Column(String(20), nullable=False)
    damage_percentage = Column(Float, nullable=False)
    damage_image_path = Column(String(500), nullable=False)
    date_of_incident = Column(Date, nullable=False)
    location_of_incident = Column(String(100), nullable=False)
    documents_path = Column(String(1000))
    fir_no = Column(String(100), nullable=True) 
    claim_date = Column(Date, nullable=True)
    remarks = Column(String(3000),nullable=True)
    approvable_reason = Column(String(3000), nullable=True)
    requested_amount = Column(Float, nullable=False)
    approvable_amount = Column(Float, nullable=True)
    approved_amount = Column(Float, nullable=True)
    claim_status = Column(String(20), nullable=False,default='in-review')

    policy = relationship("Policy", back_populates="claims")
    subject = relationship("Insurable", back_populates="claims")

    __table_args__ = (
        CheckConstraint("claim_status IN ('in-review', 'accepted', 'rejected')", name="claim_status_check"),
        CheckConstraint("severity_level IN ('Low', 'Moderate', 'High', 'Critical')", name="severity_level_check"),
    )
@event.listens_for(Claims, "before_insert")
def generate_claim_number(mapper, connection, target):
    today_str = datetime.now().strftime("%Y%m%d")

    # Count claims created today efficiently
    result = connection.execute(
        select(func.count()).where(Claims.claim_number.like(f"CLAIM-{today_str}%"))
    )
    count_today = result.scalar_one()

    target.claim_number = f"CLAIM-{today_str}{count_today + 1:03d}"


