# Student Management System - Phase 1 Foundation

This is the project foundation (Phase 1) for a Student Management System desktop application using Python, SQLite, and OOP principles.

## Project Structure

```
student_management_system/
├── database/
│   ├── __init__.py
│   └── db_manager.py       # DatabaseManager class (SQLite integration & CRUD helpers)
├── models/
│   ├── __init__.py
│   └── student.py          # Student model (business logic and database operations)
├── utils/
│   ├── __init__.py
│   └── validators.py       # Attribute validation logic (names, ages, admission numbers)
├── main.py                 # Demonstration script executing student registration, updates, and searches
└── README.md               # Project overview and instructions
```

## Requirements

- Python 3.8+
- SQLite3 (built into Python standard library)

## Running the Demonstration

To run the example usage demonstration script:

```bash
python main.py
```

This script will:
1. Initialize the SQLite database and create the required tables automatically (`students`, `subjects`, `student_subjects`, and `results`).
2. Demonstrate registering valid students.
3. Demonstrate validation checks for invalid inputs (empty name, age range violations, empty or duplicate admission numbers).
4. Perform search operations by name and admission number.
5. Update existing student records.
6. Display final contents of the database.
