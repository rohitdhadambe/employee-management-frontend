from flask import Flask, jsonify, request
from flask_cors import CORS
from db_service import (
    initialize_database,
    get_all_employees,
    create_employee,
    update_employee,
    delete_employee
)

# ... rest of your app.py code

# --- 1. Flask App Initialization ---
app = Flask(__name__)

# --- 2. Enable CORS (Crucial for Fullstack Communication) ---
CORS(app)

initialize_database()

# --- 3. First Route: Basic Health Check ---
@app.route('/', methods=['GET'])
def home():
    """Simple test route to ensure the server is running."""
    return jsonify({"message": "Employee Management API is running!", "status": "ok"}), 200

# --- 4. CRUD Routes (Placeholder for the next phase) ---

@app.route('/api/employees', methods=['GET'])
def list_employees():
    """Fetches and returns all employees from the database."""
    employees = get_all_employees()
    return jsonify([emp.to_dict() for emp in employees]), 200

@app.route('/api/employees', methods=['POST'])
def create_employee_route():
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'email', 'position']):
        return jsonify({"error": "Missing required fields (name, email, position)"}), 400

    new_employee = create_employee(data['name'], data['email'], data['position'])

    if new_employee is None:
        return jsonify({"error": "Email already exists or internal error"}), 409

    return jsonify(new_employee.to_dict()), 201

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee_route(employee_id):
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'email', 'position']):
        return jsonify({"error": "Missing required fields (name, email, position)"}), 400

    updated_employee = update_employee(employee_id, data['name'], data['email'], data['position'])

    if updated_employee is None:
        return jsonify({"error": f"Employee with ID {employee_id} not found."}), 404

    return jsonify(updated_employee.to_dict()), 200

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee_route(employee_id):
    success = delete_employee(employee_id)

    if success:
        return jsonify({"message": f"Employee with ID {employee_id} deleted successfully."}), 200
    else:
        return jsonify({"error": f"Employee with ID {employee_id} not found or could not be deleted."}), 404


if __name__ == '__main__':
    app.run(debug=True)