import sqlite3
import os
from datetime import datetime
# from helpers.config import database_path
from typing import Annotated
from database.database import get_db, sessionlocal
from database.model import User, Policy, Vehicle, Claims
# from abc import ABC, abstractmethod

# #constant DB path
# DB_PATH = database_path


# class Database(ABC):
#     # @abstractmethod
#     # def initialize_DB(self, db_path=DB_PATH):
#     #     pass

#     @abstractmethod
#     def get_by_id(self, id,db_path=DB_PATH):
#         pass

#     @abstractmethod
#     def add(self, **kwargs):
#         pass

#     @abstractmethod
#     def update(self, **kwargs):
#         pass

#     @abstractmethod
#     def get_all(self, db_path=DB_PATH) -> list:
#         pass

class user_methods():

    pass
     
class policy_methods():
    def generate_policy_number(self, db):
        today_str = datetime.now().strftime("%Y%m%d")
        count = db.query(Policy).count()
        return f"POL-{today_str}{count:02d}"
    
        

class vehicle_methods():
    pass
    
class claims_methods():
    
    def generate_claim_number(self, db ):
        today_str = datetime.now().strftime("%Y%m%d")
        count = db.query(Claims).count()
        return f"CLM-{today_str}{count:02d}"


# Call this function once at the start of your app
if __name__ == "__main__":
    
    db = sessionlocal()
    print(claims_methods().generate_claim_number(db))
    # User().initialize_DB()