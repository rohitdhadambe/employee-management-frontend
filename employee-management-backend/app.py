from flask import Flask, jsonify, request
from flask_cors import CORS
from db_service import (
    initialize_database,
    get_all_employees,
    create_employee,
    update_employee,
    delete_employee
)

app = Flask(__name__)
CORS(app)

initialize_database()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Employee Management API is running!", 
        "status": "ok"
    }), 200

@app.route('/api/employees', methods=['GET'], strict_slashes=False)
def list_employees():
    try:
        employees = get_all_employees()
        return jsonify([emp.to_dict() for emp in employees]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch employees: {str(e)}"}), 500

@app.route('/api/employees', methods=['POST'], strict_slashes=False)
def create_employee_route():
    data = request.get_json(silent=True)
    
    # Updated to 5 fields: name, email, phone, position, address
    required_fields = ['name', 'email', 'phone', 'position', 'address']
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    # FIX: Pass all 5 fields to the service layer
    new_employee = create_employee(
        name=data['name'], 
        email=data['email'], 
        phone=data['phone'],
        position=data['position'],
        address=data['address']
    )

    if new_employee is None:
        return jsonify({"error": "Email already exists or internal error"}), 409

    return jsonify(new_employee.to_dict()), 201

@app.route('/api/employees/<int:employee_id>', methods=['PUT'], strict_slashes=False)
def update_employee_route(employee_id):
    data = request.get_json(silent=True)
    
    # Updated to 5 fields: name, email, phone, position, address
    required_fields = ['name', 'email', 'phone', 'position', 'address']
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    # FIX: Pass all 5 fields to the service layer
    updated_employee = update_employee(
        employee_id=employee_id, 
        name=data['name'], 
        email=data['email'],
        phone=data['phone'],
        position=data['position'],
        address=data['address']
    )

    if updated_employee is None:
        return jsonify({
            "error": f"Employee with ID {employee_id} not found."
        }), 404

    return jsonify(updated_employee.to_dict()), 200

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'], strict_slashes=False)
def delete_employee_route(employee_id):
    success = delete_employee(employee_id)

    if success:
        return jsonify({
            "message": f"Employee with ID {employee_id} deleted successfully."
        }), 200
    else:
        return jsonify({
            "error": f"Employee with ID {employee_id} not found or could not be deleted."
        }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
