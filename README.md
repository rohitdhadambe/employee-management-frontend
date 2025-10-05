# Verto Associate Software Engineer (ASE) Challenge: Employee Data Management

## Project Description

This is a **Fullstack CRUD (Create, Read, Update, Delete)** application built as part of the Verto Associate Software Engineer Challenge. The application manages employee records, focusing on **clean code, clear RESTful API design, and robust data persistence**.

The application successfully implements the core feature (full CRUD flow with 5 data fields) and all three requested **Bonus Features** (Backend Tests, Frontend Form Validation, and Frontend Search/Filter).

### 🛠️ Tech Stack

| Component | Technology | Role | 
| ----- | ----- | ----- | 
| **Frontend** | Vue.js 3 + Quasar Framework | Responsive UI, Form Handling, State Management | 
| **Backend** | Python 3 + Flask | RESTful API Endpoints (`/api/employees`) | 
| **Database** | SQLite | File-based data persistence (as required) | 
| **Testing** | Pytest | Backend Test Automation (Bonus) | 

### Data Model (5 Fields)

The Employee model consists of the following required fields: `id` (PK), **`name`**, **`email`** (Unique), **`phone`**, **`position`**, and **`address`**.

---

## 🚀 Setup and Run Instructions

This is a dual-component application that requires running the backend (Python) and frontend (Node/Quasar) simultaneously.

### Prerequisites

You must have **Python 3.x** and **Node.js/npm (or yarn)** installed.

### 1. Backend Setup (Flask API)

1.  Navigate to the backend directory:

    ```bash
    cd employee-management-backend
    ```

2.  Create and activate the virtual environment:

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Run the Flask API:

    ```bash
    # RECOMMENDED: Use the Flask CLI
    flask run
    
    # ALTERNATIVE: Run the file directly
    python app.py
    ```

    *(The API will run on `http://127.0.0.1:5000`)*

### 2. Frontend Setup (Vue/Quasar)

1.  Open a **second terminal window** and navigate to the project root:

    ```bash
    cd frontend
    ```

2.  Install Node.js dependencies:

    ```bash
    npm install
    # OR yarn install
    ```

3.  Ensure the API endpoint is configured in your `.env` file (located in the `frontend` directory): `VITE_API_BASE_URL="http://127.0.0.1:5000/api"`

4.  **Start the app in development mode:**

    ```bash
    quasar dev
    ```

    *(The web application will open in your browser, typically at `http://localhost:8080`)*

---

## ✅ Running Test Cases (Bonus Feature)

The backend includes a comprehensive test suite using **Pytest** (6 passing tests) to validate all API endpoints, including data validation and conflict handling.

1.  Ensure the Flask server is **STOPPED** and your Python virtual environment is **ACTIVE** in the `employee-management-backend` directory.

2.  Run the test command:

    ```bash
    pytest test_app.py
    ```

    **(Expected result: 6 passed)**

---

## 💡 Assumptions and Design Choices

1.  **Tech Stack Alignment:** Used **Python/Flask** as the accepted OOP language, demonstrating versatility, and **Vue/Quasar** for modern, responsive frontend development.

2.  **Data Isolation (Testing):** The Pytest setup ensures robust **test isolation** by calling `clear_employees()` before every test function, guaranteeing a clean slate and reliable results.

3.  **Bonus Feature Implementation:**
    * **Frontend Validation:** Implemented using Quasar's declarative `:rules` attribute for immediate user feedback.
    * **Search/Filter:** Handled efficiently using a Vue **`computed`** property to perform client-side filtering on all 5 employee fields.

4.  **Error Handling:** API errors (e.g., 409 Conflict for duplicate email) are caught on the frontend and displayed to the user via Quasar's non-blocking notification system.
```eof