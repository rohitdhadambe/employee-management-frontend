from flask import Flask, jsonify
from flask_cors import CORS
from db_service import initialize_database, get_all_employees 

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


if __name__ == '__main__':
    app.run(debug=True)