import sqlite3
import os
from datetime import datetime

def init_db(db_path="insurance.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Create policies table with policy_number
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS policies (
            policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_number TEXT UNIQUE NOT NULL,
            policy_holder TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            premium REAL NOT NULL,
            status TEXT CHECK(status IN ('active', 'inactive')) NOT NULL
        )
    """)
    # Create vehicles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_id INTEGER NOT NULL,
            image_path TEXT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year_of_purchase INTEGER NOT NULL,
            FOREIGN KEY(policy_id) REFERENCES policies(policy_id)
        )
    """)
    conn.commit()
    conn.close()

def generate_policy_number(db_path="insurance.db"):
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

def add_policy(policy_holder, start_date, end_date, premium, status, db_path="insurance.db"):
    policy_number = generate_policy_number(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO policies (policy_number, policy_holder, start_date, end_date, premium, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (policy_number, policy_holder, start_date, end_date, premium, status))
    conn.commit()
    policy_id = cursor.lastrowid
    conn.close()
    return policy_id, policy_number

def get_policy_by_id(policy_id, db_path="insurance.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM policies WHERE policy_id = ?", (policy_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_policies_by_holder(policy_holder, db_path="insurance.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM policies WHERE policy_holder = ?", (policy_holder,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_policies_by_vehicle_make(make, db_path="insurance.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.* FROM policies p
        JOIN vehicles v ON p.policy_id = v.policy_id
        WHERE v.make = ?
    """, (make,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_policies_by_vehicle_model(model, db_path="insurance.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.* FROM policies p
        JOIN vehicles v ON p.policy_id = v.policy_id
        WHERE v.model = ?
    """, (model,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_policies(db_path="insurance.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM policies")
    results = cursor.fetchall()
    conn.close()
    return results

def add_dummy_policies(db_path="insurance.db"):
    # Example dummy data
    dummy_data = [
        ("Alice Johnson", "2024-07-01", "2025-07-01", 12000.0, "active"),
        ("Bob Smith", "2024-06-15", "2025-06-15", 9500.0, "inactive"),
        ("Charlie Lee", "2024-05-10", "2025-05-10", 15000.0, "active"),
        ("Diana Prince", "2024-07-09", "2025-07-09", 11000.0, "active"),
    ]
    for policy_holder, start_date, end_date, premium, status in dummy_data:
        add_policy(policy_holder, start_date, end_date, premium, status, db_path)

def update_policy(policy_id, policy_holder, start_date, end_date, premium, status, db_path="insurance.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE policies
        SET policy_holder = ?, start_date = ?, end_date = ?, premium = ?, status = ?
        WHERE policy_id = ?
    """, (policy_holder, start_date, end_date, premium, status, policy_id))
    conn.commit()
    conn.close()

def add_vehicle(policy_id, image_path, make, model, year_of_purchase, db_path="insurance.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vehicles (policy_id, image_path, make, model, year_of_purchase)
        VALUES (?, ?, ?, ?, ?)
    """, (policy_id, image_path, make, model, year_of_purchase))
    conn.commit()
    conn.close()

# Call this function once at the start of your app
if __name__ == "__main__":
    os.makedirs("vehicle_images", exist_ok=True)
    init_db()
    add_dummy_policies()
