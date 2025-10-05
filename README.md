Verto Associate Software Engineer (ASE) Challenge: Employee Data Management
Project Description
This is a Fullstack CRUD (Create, Read, Update, Delete) application built as part of the Verto Associate Software Engineer Challenge. The application manages employee records, focusing on clean code, clear RESTful API design, and robust data persistence.

The application successfully implements the core feature (full CRUD flow) and all three requested Bonus Features (Backend Tests, Frontend Form Validation, and Frontend Search/Filter).

🛠️ Tech Stack
Frontend: Vue.js 3 (Composition API) with Quasar Framework

Backend: Python 3 + Flask (for the RESTful API)

Database: SQLite (File-based persistence, as required)

Data Model (5 Fields)
The Employee model consists of the following required fields:

id (Auto-generated Primary Key)

name (String, Required)

email (String, Required, Unique)

phone (String, Required)

position (String, Required)

address (String, Required)

🚀 Setup and Run Instructions
This is a dual-component application that requires running the backend (Python) and frontend (Node/Quasar) simultaneously.

Prerequisites
You must have Python 3.x and Node.js/npm (or yarn) installed.

1. Backend Setup (Flask API)
Navigate to the backend directory:

cd employee-management-backend


Create and activate the virtual environment:

Windows: python -m venv venv then .\venv\Scripts\activate

Linux/macOS: python3 -m venv venv then source venv/bin/activate

Install Python dependencies:

pip install -r requirements.txt


Run the Flask API:

# RECOMMENDED: Use the Flask CLI
flask run

# ALTERNATIVE: Run the file directly
# python app.py

(The API will run on http://127.0.0.1:5000)

2. Frontend Setup (Vue/Quasar)
Open a second terminal window and navigate to the project root:

cd ..  # Go back to the root directory containing the 'frontend' folder
cd frontend


Install Node.js dependencies:

npm install
# OR yarn install


Ensure the API endpoint is configured in your .env file (located in the frontend directory):

VITE_API_BASE_URL="[http://127.0.0.1:5000/api](http://127.0.0.1:5000/api)"


Run the Quasar development server:

quasar dev


(The web application will open in your browser, typically at http://localhost:8080)

✅ Running Test Cases (Bonus Feature)
The backend includes a comprehensive test suite using Pytest to validate all API endpoints (GET, POST, PUT, DELETE) and core business logic (e.g., duplicate email check, data validation).

Ensure the Flask server is STOPPED and your Python virtual environment is ACTIVE in the employee-management-backend directory.

Run the test command:

pytest test_app.py


(Expected result: 6 passed)

💡 Assumptions and Design Choices
Tech Stack: Used Python/Flask (OOP language) and Vue/Quasar to demonstrate proficiency in both backend and modern frontend development.

State Management: Frontend state management is handled efficiently using Vue 3's Composition API (ref, computed) directly within the component, avoiding unnecessary complexity for an application of this scale.

Data Isolation (Testing): The test environment uses the client fixture to aggressively clean the database (clear_employees()) before every test execution, guaranteeing test isolation and reliability.

Error Handling: API errors (e.g., 409 Conflict for duplicate email, 404 Not Found) are caught on the frontend using Axios and displayed to the user via Quasar's non-blocking notification system ($q.notify).

Bonus Feature Implementation:

Frontend Validation: Implemented using Quasar's :rules attribute on form inputs for immediate user feedback.

Search/Filter: Implemented using a Vue computed property to instantly filter the displayed employee list based on name, email, or position, providing a smooth UX.