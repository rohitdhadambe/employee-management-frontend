import pytest
import os
import tempfile
import sqlite3
import json

from app import app
from db_service import initialize_database, create_employee, get_db_connection, DATABASE_NAME

TEST_DATABASE_NAME = 'test_employee_data.db'

def get_test_db_connection():
    conn = sqlite3.connect(TEST_DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_test_database():
    conn = get_test_db_connection()
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
    finally:
        conn.close()

@pytest.fixture
def client():
    global DATABASE_NAME
    original_db_name = DATABASE_NAME
    DATABASE_NAME = TEST_DATABASE_NAME

    if os.path.exists(TEST_DATABASE_NAME):
        os.remove(TEST_DATABASE_NAME)
    initialize_test_database()
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

    os.remove(TEST_DATABASE_NAME)
    DATABASE_NAME = original_db_name

def test_0_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

def test_1_create_and_read_employee(client):
    new_employee_data = {
        'name': 'Test User',
        'email': 'testuser@verto.com',
        'position': 'Test Engineer'
    }
    response = client.post('/api/employees', json=new_employee_data)
    assert response.status_code == 201
    created_emp = response.get_json()
    assert created_emp['name'] == 'Test User'
    assert created_emp['id'] is not None

    response_get = client.get('/api/employees')
    assert response_get.status_code == 200
    employees = response_get.get_json()
    assert len(employees) == 1
    assert employees[0]['email'] == 'testuser@verto.com'

    return created_emp['id']

def test_2_update_employee(client):
    emp_id = test_1_create_and_read_employee(client)
    update_data = {
        'name': 'Updated Test User',
        'email': 'updated@verto.com',
        'position': 'Senior Test Engineer'
    }
    response = client.put(f'/api/employees/{emp_id}', json=update_data)
    assert response.status_code == 200
    updated_emp = response.get_json()
    assert updated_emp['name'] == 'Updated Test User'
    assert updated_emp['email'] == 'updated@verto.com'

    response_get = client.get('/api/employees')
    employees = response_get.get_json()
    assert employees[0]['email'] == 'updated@verto.com'

def test_3_delete_employee(client):
    emp_id = test_1_create_and_read_employee(client)

    response = client.delete(f'/api/employees/{emp_id}')
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()['message']

    response_get = client.get('/api/employees')
    employees = response_get.get_json()
    assert len(employees) == 0

    response_not_found = client.delete(f'/api/employees/{emp_id}')
    assert response_not_found.status_code == 404

def test_4_invalid_create(client):
    bad_data = {
        'name': 'Incomplete',
        'email': 'bad@verto.com'
    }
    response = client.post('/api/employees', json=bad_data)
    assert response.status_code == 400

    valid_data = {'name': 'Dupe User', 'email': 'dupe@verto.com', 'position': 'Dev'}
    client.post('/api/employees', json=valid_data)
    response_dupe = client.post('/api/employees', json=valid_data)
    assert response_dupe.status_code == 409

@pytest.fixture
def employee_id_to_test(client):
    """Creates a unique employee and yields their ID for testing updates/deletions."""
    unique_email = f"temp_user_{client}_@verto.com" 
    
    new_employee_data = {
        'name': 'Fixture User',
        'email': unique_email,
        'position': 'Fixture Position'
    }
    response = client.post('/api/employees', json=new_employee_data)
    
    assert response.status_code == 201
    
    created_emp = response.get_json()
    yield created_emp['id']
    
def test_1_create_and_read_employee(client):
    new_employee_data = {
        'name': 'Test User',
        'email': 'testuser@verto.com',
        'position': 'Test Engineer'
    }

def test_2_update_employee(client, employee_id_to_test):
    """Tests PUT (Update) operation."""
    emp_id = employee_id_to_test 
    
    update_data = {
        'name': 'Updated Test User',
        'position': 'Senior Test Engineer'
    }
    response = client.put(f'/api/employees/{emp_id}', json=update_data)
    
    assert response.status_code == 200 
    updated_emp = response.get_json()
    assert updated_emp['name'] == 'Updated Test User'
    assert updated_emp['email'] == f'updated_{emp_id}@verto.com'

def test_3_delete_employee(client, employee_id_to_test):
    """Tests DELETE operation."""
    emp_id = employee_id_to_test 
    
    response = client.delete(f'/api/employees/{emp_id}')
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()['message']
    