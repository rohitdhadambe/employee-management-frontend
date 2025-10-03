# db_service.py

import sqlite3
from typing import List, Dict, Optional

DATABASE_NAME = 'employee_data.db'

# Represents the structure of a single employee record
class Employee:
    def __init__(self, name: str, email: str, position: str, id: Optional[int] = None):
        self.id = id
        self.name = name
        self.email = email
        self.position = position

    # Helper method to convert the object to a dictionary (useful for JSON response)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "position": self.position
        }

# ---  Database Connection and Initialization ---

def get_db_connection():
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Creates the employee table if it does not exist."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                position TEXT NOT NULL
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

# ---  Core Database Operations (CRUD Service Layer) ---

def get_all_employees() -> List[Employee]:
    """Returns a list of all Employee objects."""
    initialize_database() # Ensure table exists before querying
    conn = get_db_connection()
    employees: List[Employee] = []
    try:
        rows = conn.execute("SELECT * FROM employees;").fetchall()
        for row in rows:
            employees.append(Employee(
                id=row['id'],
                name=row['name'],
                email=row['email'],
                position=row['position']
            ))
    except Exception as e:
        print(f"Error fetching employees: {e}")
    finally:
        conn.close()
    return employees

# Call this once to ensure the database file is created and the table exists
initialize_database() 
print(f"Database initialized: {DATABASE_NAME}")