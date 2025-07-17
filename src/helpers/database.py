import sqlite3
import os
from datetime import datetime
from helpers.config import database_path
from abc import ABC, abstractmethod

#constant DB path
DB_PATH = database_path


class Database(ABC):
    # @abstractmethod
    # def initialize_DB(self, db_path=DB_PATH):
    #     pass

    @abstractmethod
    def get_by_id(self, id,db_path=DB_PATH):
        pass

    @abstractmethod
    def add(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def get_all(self, db_path=DB_PATH) -> list:
        pass

class User(Database):
    def __init__(self, db_path=DB_PATH ):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        create_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            usertype TEXT NOT NULL DEFAULT 'user' CHECK(usertype IN ('admin', 'user', 'agent')),
            username TEXT UNIQUE NOT NULL,
            firstname TEXT NOT NULL,
            middlename TEXT,
            lastname TEXT NOT NULL,
            password TEXT NOT NULL,
            dateofbirth Date,
            phone TEXT,
            email TEXT UNIQUE NOT NULL,
            address TEXT
        )
        """
        cursor.execute(create_query)
        conn.commit()
        conn.close()

    def get_by_id(self, id, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def add(self, **kwargs):
        usertype = kwargs.get('usertype', 'user')  # Default to 'user' if not provided
        username = kwargs.get('username')
        firstname = kwargs.get('firstname')
        middlename = kwargs.get('middlename')
        lastname = kwargs.get('lastname')
        password = kwargs.get('password')
        dateofbirth = kwargs.get('dateofbirth')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        address = kwargs.get('address')
        db_path = kwargs.get('db_path', DB_PATH)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (usertype, username, firstname, middlename, lastname, password, dateofbirth, phone, email, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ( username, firstname, middlename, lastname, password, dateofbirth, phone, email, address))
        conn.commit()
        conn.close()

    def update(self, **kwargs):
        user_id = kwargs.get('user_id')
        usertype = kwargs.get('usertype', 'user')  # Default to 'user' if not provided
        username = kwargs.get('username')
        firstname = kwargs.get('firstname')
        middlename = kwargs.get('middlename')
        lastname = kwargs.get('lastname')
        password = kwargs.get('password')
        dateofbirth = kwargs.get('dateofbirth')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        address = kwargs.get('address')
        db_path = kwargs.get('db_path', DB_PATH)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET usertype=?, username = ?, firstname = ?, middlename = ?, lastname = ?, password = ?, dateofbirth = ?, phone = ?, email = ?, address = ?
            WHERE user_id = ?
        """, (usertype, username, firstname, middlename, lastname, password, dateofbirth, phone, email, address, user_id))
        conn.commit()
        conn.close()
    
    def get_all(self, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        conn.close()
        return results
     


class Policy(Database):
    def __init__(self, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        create_query = """
        CREATE TABLE IF NOT EXISTS policies (
            policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_number TEXT UNIQUE NOT NULL,
            policy_holder TEXT NOT NULL,
            user_id INTEGER,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            premium REAL NOT NULL,
            status TEXT CHECK(status IN ('active', 'inactive')) NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """
        cursor.execute(create_query)
        conn.commit()
        conn.close()

    def get_id(self, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(policy_id) FROM policies")
        result = cursor.fetchone()[0]
        conn.close()
        return result if result is not None else 0

    def generate_policy_number(self, db_path=DB_PATH):
        today_str = datetime.now().strftime("%Y%m%d")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM policies WHERE policy_number LIKE ?",
            (f"PLC-{today_str}%",)
        )
        count = cursor.fetchone()[0] + 1
        conn.close()
        return f"PLC-{today_str}{count:02d}"
    
    def add(self, **kwargs):
        policy_holder = kwargs.get('policy_holder')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        premium = kwargs.get('premium')
        status = kwargs.get('status')
        user_id = kwargs.get('user_id')  # Add this line
        db_path = kwargs.get('db_path', DB_PATH)
        policy_number = self.generate_policy_number(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO policies (policy_number, policy_holder, user_id, start_date, end_date, premium, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (policy_number, policy_holder, user_id, start_date, end_date, premium, status))
        conn.commit()
        policy_id = cursor.lastrowid
        conn.close()

    def get_by_id(self, id, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM policies WHERE policy_id = ?", (id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def update(self, **kwargs):
        policy_id = kwargs.get('policy_id')
        policy_holder = kwargs.get('policy_holder')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        premium = kwargs.get('premium')
        status = kwargs.get('status')
        db_path = kwargs.get('db_path', DB_PATH)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE policies
            SET policy_holder = ?, start_date = ?, end_date = ?, premium = ?, status = ?
            WHERE policy_id = ?
        """, (policy_holder, start_date, end_date, premium, status, policy_id))
        conn.commit()
        conn.close()

    def get_all(self, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM policies")
        results = cursor.fetchone()
        conn.close()
        return results

class Vehicle(Database):
    def __init__(self, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        create_query = """
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_id INTEGER NOT NULL,
            typeofvehicle TEXT CHECK(typeofvehicle IN ('fourwheeler', 'threewheeler', 'twowheeler', 'other')) NOT NULL,
            image_path TEXT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year_of_purchase INTEGER NOT NULL,
            FOREIGN KEY(policy_id) REFERENCES policies(policy_id)
        )
        """
        cursor.execute(create_query)
        conn.commit()
        conn.close()

    def add(self, **kwargs):
        policy_id = kwargs.get('policy_id')
        typeofvehicle = kwargs.get('typeofvehicle', 'other')
        image_path = kwargs.get('image_path')
        make = kwargs.get('make')
        model = kwargs.get('model')
        year_of_purchase = kwargs.get('year_of_purchase')
        db_path = kwargs.get('db_path', DB_PATH)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vehicles (policy_id,typeofvehicle, image_path, make, model, year_of_purchase)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (policy_id,typeofvehicle, image_path, make, model, year_of_purchase))
        conn.commit()
        conn.close()

    def get_by_id(self, id, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE vehicle_id = ?", (id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def update(self, **kwargs):
        vehicle_id = kwargs.get('vehicle_id')
        policy_id = kwargs.get('policy_id')
        typeofvehicle = kwargs.get('typeofvehicle', 'other')
        image_path = kwargs.get('image_path')
        make = kwargs.get('make')
        model = kwargs.get('model')
        year_of_purchase = kwargs.get('year_of_purchase')
        db_path = kwargs.get('db_path', DB_PATH)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE vehicles
            SET policy_id = ?, typeofvehicle=?, image_path = ?, make = ?, model = ?, year_of_purchase = ?
            WHERE vehicle_id = ?
        """, (policy_id, typeofvehicle, image_path, make, model, year_of_purchase, vehicle_id))
        conn.commit()
        conn.close()

    def get_all(self, db_path=DB_PATH):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles")
        results = cursor.fetchall()
        conn.close()
        return results
    
class Claims(Database):
    pass


def add_dummy_policies(db_path=DB_PATH):
    # Example dummy data
    dummy_data = [
        ("Alice Johnson", "2024-07-01", "2025-07-01", 12000.0, "active"),
        ("Bob Smith", "2024-06-15", "2025-06-15", 9500.0, "inactive"),
        ("Charlie Lee", "2024-05-10", "2025-05-10", 15000.0, "active"),
        ("Diana Prince", "2024-07-09", "2025-07-09", 11000.0, "active"),
    ]
    for policy_holder, start_date, end_date, premium, status in dummy_data:
        Policy().add(policy_holder=policy_holder, start_date=start_date, end_date=end_date, premium=premium, status=status, db_path=db_path)

# Call this function once at the start of your app
if __name__ == "__main__":
    pass