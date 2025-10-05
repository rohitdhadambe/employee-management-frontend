import pytest
import os
import sqlite3
import json

from app import app
from db_service import create_employee, get_db_connection, DATABASE_NAME, clear_employees 

TEST_DATABASE_NAME = 'test_employee_data.db'

def get_test_db_connection():
    conn = sqlite3.connect(TEST_DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_test_database():
    conn = get_test_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                position TEXT NOT NULL,
                address TEXT NOT NULL
            );
        """)
        conn.commit()
    finally:
        conn.close()

@pytest.fixture
def client():
    global DATABASE_NAME
    original_db_name = DATABASE_NAME
    DATABASE_NAME = TEST_DATABASE_NAME

    if not os.path.exists(TEST_DATABASE_NAME):
        initialize_test_database()
        
    app.config['TESTING'] = True
    with app.test_client() as client:
        clear_employees()
        yield client

    DATABASE_NAME = original_db_name


@pytest.fixture
def employee_id_to_test(client):
    unique_email = f"fixture_user_{os.getpid()}@verto.com" 
    
    new_employee_data = {
        'name': 'Fixture User',
        'email': unique_email,
        'phone': '1112223333',
        'position': 'Fixture Position',
        'address': 'Test Address 123'
    }
    response = client.post('/api/employees', json=new_employee_data)
    
    assert response.status_code == 201, f"Fixture failed to create employee: {response.get_data(as_text=True)}"
    
    created_emp = response.get_json()
    yield created_emp['id']
    
def test_0_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

def test_1_create_and_read_employee(client):
    new_employee_data = {
        'name': 'Test User A',
        'email': 'testuser_a@verto.com',
        'phone': '5551234567',
        'position': 'Test Engineer',
        'address': 'Test Address A'
    }
    response = client.post('/api/employees', json=new_employee_data)
    assert response.status_code == 201
    
    response_get = client.get('/api/employees')
    assert response_get.status_code == 200
    employees = response_get.get_json()
    assert len(employees) == 1
    assert employees[0]['email'] == 'testuser_a@verto.com'
    assert employees[0]['phone'] == '5551234567'


def test_2_update_employee_success(client, employee_id_to_test):
    emp_id = employee_id_to_test
    
    update_data = {
        'name': 'Updated Test User',
        'email': f'updated_{emp_id}_email@verto.com',
        'phone': '9876543210',
        'position': 'Senior Test Engineer',
        'address': 'Updated Test Address'
    }
    response = client.put(f'/api/employees/{emp_id}', json=update_data)
    assert response.status_code == 200
    
    response_get_all = client.get('/api/employees')
    employees = response_get_all.get_json()
    assert len(employees) == 1
    updated_emp = employees[0]
    
    assert updated_emp['position'] == 'Senior Test Engineer'
    assert updated_emp['phone'] == '9876543210'
    assert updated_emp['address'] == 'Updated Test Address'


def test_3_delete_employee_success(client, employee_id_to_test):
    emp_id = employee_id_to_test
    
    response = client.delete(f'/api/employees/{emp_id}')
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()['message']

    response_get = client.get('/api/employees')
    assert len(response_get.get_json()) == 0

    response_not_found = client.delete(f'/api/employees/{emp_id}')
    assert response_not_found.status_code == 404

def test_4_invalid_create_and_conflict(client):
    bad_data = {
        'name': 'Incomplete',
        'email': 'bad@verto.com',
        'position': 'Missing Data',
        'address': 'Some address'
    }
    response_bad = client.post('/api/employees', json=bad_data)
    assert response_bad.status_code == 400

    valid_data = {
        'name': 'Dupe User',
        'email': 'dupe@verto.com',
        'phone': '5555555555',
        'position': 'Dev',
        'address': 'Dupe Address'
    }
    client.post('/api/employees', json=valid_data)
    response_dupe = client.post('/api/employees', json=valid_data)
    
    assert response_dupe.status_code == 409
    
def test_5_update_invalid_id(client):
    update_data = {
        'name': 'Missing User',
        'email': 'missing@verto.com',
        'phone': '0000000000',
        'position': 'Ghost',
        'address': 'No address'
    }
    response_404 = client.put(f'/api/employees/99999', json=update_data)
    assert response_404.status_code == 404
