import sqlite3
from typing import List, Optional

DATABASE_NAME = 'employee_data.db'

class Employee:
    def __init__(self, name: str, email: str, phone: str, position: str, address: str, id: Optional[int] = None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.position = position
        self.address = address

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "position": self.position,
            "address": self.address
        }

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            cursor.execute("""
                CREATE TABLE employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL,
                    position TEXT NOT NULL,
                    address TEXT NOT NULL
                );
            """)
            conn.commit()
        else:
            cursor.execute("PRAGMA table_info(employees)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'phone' not in columns:
                cursor.execute("ALTER TABLE employees ADD COLUMN phone TEXT DEFAULT ''")
                conn.commit()
            
            if 'address' not in columns:
                cursor.execute("ALTER TABLE employees ADD COLUMN address TEXT DEFAULT ''")
                conn.commit()
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_all_employees() -> List[Employee]:
    conn = get_db_connection()
    employees: List[Employee] = []
    try:
        rows = conn.execute("SELECT * FROM employees;").fetchall()
        for row in rows:
            employees.append(Employee(
                id=row['id'],
                name=row['name'],
                email=row['email'],
                phone=row['phone'],
                position=row['position'],
                address=row['address']
            ))
    except Exception as e:
        print(f"Error fetching employees: {e}")
    finally:
        conn.close()
    return employees

def create_employee(name: str, email: str, phone: str, position: str, address: str) -> Optional[Employee]:
    conn = get_db_connection()
    try:
        existing = conn.execute("SELECT id FROM employees WHERE email = ?", (email,)).fetchone()
        if existing:
            return None

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (name, email, phone, position, address) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, position, address)
        )
        conn.commit()
        new_id = cursor.lastrowid
        return Employee(id=new_id, name=name, email=email, phone=phone, position=position, address=address)
    except Exception as e:
        print(f"Error creating employee: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def update_employee(employee_id: int, name: str, email: str, phone: str, position: str, address: str) -> Optional[Employee]:
    conn = get_db_connection()
    try:
        existing = conn.execute("SELECT id FROM employees WHERE id = ?", (employee_id,)).fetchone()
        if not existing:
            return None

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employees SET name = ?, email = ?, phone = ?, position = ?, address = ? WHERE id = ?",
            (name, email, phone, position, address, employee_id)
        )
        conn.commit()
        return Employee(id=employee_id, name=name, email=email, phone=phone, position=position, address=address)
    except Exception as e:
        print(f"Error updating employee: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def delete_employee(employee_id: int) -> bool:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        return deleted
    except Exception as e:
        print(f"Error deleting employee: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def clear_employees():
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM employees;")
        conn.commit()
    except Exception as e:
        print(f"Error clearing employees: {e}")
    finally:
        conn.close()

initialize_database()
