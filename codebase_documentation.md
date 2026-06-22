# Admission Guard - Codebase Documentation

Welcome to the **Admission Guard Student Management System** documentation. This document provides a detailed overview of the application's structure, files, services, and architecture flow.

---

## Codebase Overview

Admission Guard is designed as a desktop application using Python, Tkinter, and SQLite. It follows an Object-Oriented Programming (OOP) architecture with clear separation of concerns (Layered Architecture):

```
+-------------------------------------------------------+
|                       UI LAYER                        |
|   (main_window.py, login_form.py, module frames)      |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|                    SERVICES LAYER                     |
|  (auth_service.py, student_service.py, etc.)          |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|                     MODELS LAYER                      |
|  (user.py, student.py, subject.py, result.py, etc.)   |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|                    DATABASE LAYER                     |
|                   (db_manager.py)                     |
+-------------------------------------------------------+
```

---

## Directory Structure

Here is the directory structure of the application:

```
student_management_system/
│
├── main.py                     # Application entrypoint
├── view_database.py            # SQLite utility command-line script
│
├── database/                   # Database connection and table setup
│   ├── __init__.py
│   └── db_manager.py           # Core SQLite execution manager
│
├── models/                     # Data entities (OOP classes)
│   ├── __init__.py
│   ├── user.py                 # User security entity
│   ├── student.py              # Student entity
│   ├── subject.py              # Subject entity
│   ├── student_subject.py      # Junction / Assignment entity
│   └── result.py               # Academic result entity
│
├── services/                   # Business logic and query delegation
│   ├── __init__.py
│   ├── auth_service.py         # Login and default admin creation
│   ├── student_service.py      # Student coordination
│   ├── subject_service.py      # Subject coordination
│   ├── assignment_service.py   # Subject assignments coordination
│   ├── result_service.py       # Marks and mean score calculation
│   └── search_service.py       # Profiles building and search directory
│
├── ui/                         # User Interface Layer (Tkinter views)
│   ├── __init__.py
│   ├── main_window.py          # Dashboard wrapper (tk.Tk) & sidebar navigation
│   ├── login_form.py           # Login dialog popup overlay (tk.Toplevel)
│   ├── dashboard_view.py       # Inside frame displaying metrics (tk.Frame)
│   ├── student_form.py         # Inside frame for student registration (tk.Frame)
│   ├── subject_form.py         # Inside frame for subject records (tk.Frame)
│   ├── subject_assignment_form.py # Inside frame for subject assignment (tk.Frame)
│   ├── result_form.py          # Inside frame for results recording (tk.Frame)
│   ├── search_view.py          # Inside frame for student directory search (tk.Frame)
│   └── student_profile_view.py # Detailed profile dialog popup overlay (tk.Toplevel)
│
└── utils/                      # Helper files and custom validators
    ├── __init__.py
    └── validators.py           # Input validations & uniqueness rules
```

---

## Detailed Directory and File Breakdown

### 1. Root Files

*   **[main.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/main.py)**
    *   **Purpose**: The main bootstrapper of the application.
    *   **Key Responsibilities**:
        *   Instantiates the single `DatabaseManager` pointing to `student_system.db`.
        *   Initializes all service modules (`AuthService`, `StudentService`, `SubjectService`, `AssignmentService`, `ResultService`, `SearchService`).
        *   Instantiates `MainWindow` passing the active service instances.
        *   Triggers the main Tkinter event loop (`app.mainloop()`).
*   **[view_database.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/view_database.py)**
    *   **Purpose**: A debugging script to inspect database data on the terminal.
    *   **Key Responsibilities**: Connects directly to `student_system.db` and prints formatted tables of students, subjects, and assignments to the standard output.

---

### 2. Database Directory

*   **[database/db_manager.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/database/db_manager.py)**
    *   **Purpose**: Coordinates SQL connection pool, database creation, table structure setup, and queries execution.
    *   **Key Responsibilities**:
        *   Creates `student_system.db` folder and database if it does not exist.
        *   Ensures SQLite foreign keys constraint checks are enabled on connection (`PRAGMA foreign_keys = ON;`).
        *   Runs `create_tables()` to define the schema for `students`, `subjects`, `student_subjects`, `results`, and `users` tables.
        *   Exposes generic utility methods: `execute_query()`, `fetch_all()`, and `fetch_one()`.

---

### 3. Models Directory

Models are OOP classes representing database table rows. They are responsible for low-level database inserts and updates.

*   **[models/user.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/models/user.py)**
    *   **Attributes**: `user_id`, `username`, `password`.
    *   **Methods**:
        *   `create_user(db_manager)`: Registers a user with credentials. Throws if username exists.
        *   `get_user(db_manager, username)` (staticmethod): Retrieves user instance by username.
        *   `validate_user(password)`: Verifies username password.
*   **[models/student.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/models/student.py)**
    *   **Attributes**: `student_id`, `admission_no`, `full_name`, `age`, `gender`, `date_of_admission`.
    *   **Methods**:
        *   `register_student(db_manager)`: Performs field-level validation and registers student.
        *   `update_student(db_manager)`: Updates details in database.
        *   `search_student(db_manager, search_term)` (staticmethod): Performs query matching name or admission no.
        *   `get_by_id(db_manager, student_id)` (staticmethod): Selects a student by primary key.
*   **[models/subject.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/models/subject.py)**
    *   **Attributes**: `subject_id`, `subject_name`, `subject_code`.
    *   **Methods**:
        *   `save_subject(db_manager)`: Saves subject. Validates code prefix/uniqueness.
        *   `update_subject(db_manager)`: Updates subject name.
        *   `get_all_subjects(db_manager)` (staticmethod): Fetches all database subjects.
*   **[models/student_subject.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/models/student_subject.py)**
    *   **Attributes**: `student_id`, `subject_id`.
    *   **Methods**:
        *   `assign_subject(db_manager)`: Creates junction table mapping between student and subject.
        *   `remove_assignment(db_manager)`: Removes the subject mapping.
*   **[models/result.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/models/result.py)**
    *   **Attributes**: `result_id`, `student_id`, `subject_id`, `assessment_mark`, `exam_mark`, `total_mark`.
    *   **Methods**:
        *   `save_result(db_manager)`: Saves recorded marks.
        *   `update_result(db_manager)`: Updates assessment or exam marks.

---

### 4. Services Directory

Services coordinate actions between UI frames and database models, holding business logic checks.

*   **[services/auth_service.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/services/auth_service.py)**
    *   **Responsibilities**:
        *   `authenticate(username, password)`: Checks inputs and logs in users, setting `current_user`.
        *   `create_default_admin()`: Creates default administrator `admin` / `admin123` if the DB is fresh and has no user records.
        *   `logout()`: Destroys current session.
*   **[services/student_service.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/services/student_service.py)**
    *   **Responsibilities**:
        *   `create_student(...)`: Validates and registers students.
        *   `get_student(student_id)`: Fetches details for profile.
        *   `get_all_students()`: Lists student directory.
*   **[services/subject_service.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/services/subject_service.py)**
    *   **Responsibilities**:
        *   `create_subject(name)`: Generates auto-generated code and registers subject.
        *   `update_subject(subject_id, new_name)`: Updates subject name.
        *   `delete_subject(subject_id)`: Removes subject.
*   **[services/assignment_service.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/services/assignment_service.py)**
    *   **Responsibilities**:
        *   `get_available_subjects(student_id)`: List of subjects **not** assigned to the student.
        *   `get_assigned_subjects(student_id)`: List of subjects currently assigned.
        *   `assign_subject_to_student(student_id, subject_id)`: Assigns subject.
        *   `remove_subject_from_student(student_id, subject_id)`: Removes subject.
*   **[services/result_service.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/services/result_service.py)**
    *   **Responsibilities**:
        *   `save_result(...)`: Saves student marks. Validates that marks are within bounds (Assessment: 0-30, Exam: 0-70).
        *   `update_result(...)`: Edits student marks.
        *   `get_student_results(student_id)`: Lists student graded records.
        *   `calculate_student_mean(student_id)`: Computes the overall average score (Sum of Total Marks ÷ Number of Graded Subjects).
*   **[services/search_service.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/services/search_service.py)**
    *   **Responsibilities**:
        *   `search_by_admission_no(...)`: Performs partial search queries on admission numbers.
        *   `search_by_name(...)`: Performs partial search queries on student names.
        *   `get_student_profile(student_id)`: Retrieves a student's personal information details.
        *   `get_student_subjects(student_id)`: Retrieves list of assigned subjects.
        *   `get_student_results(student_id)`: Retrieves recorded marks list.
        *   `calculate_student_mean(student_id)`: Accesses average score.

---

### 5. UI Directory

The UI layout is a single-window desktop dashboard. [MainWindow](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/main_window.py) manages a left-hand navigation sidebar and a right-hand main content container frame.

*   **[ui/main_window.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/main_window.py)**
    *   **Base class**: `tk.Tk` (Root Window).
    *   **Responsibilities**: Hides itself on launch (`self.withdraw()`) and launches the login window popup overlay. Upon successful authentication, deiconifies itself, displaying the sidebar menu and loading the active frame (defaulting to the Dashboard). Switches frames using `switch_to_tab()`.
*   **[ui/login_form.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/login_form.py)**
    *   **Base class**: `tk.Toplevel` (Modal Window).
    *   **Responsibilities**: Prompts credentials inputs (username and password with mask character protection). Validates inputs against `AuthService` and invokes login success callback.
*   **[ui/dashboard_view.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/dashboard_view.py)**
    *   **Base class**: `tk.Frame` (Dashboard View Panel).
    *   **Responsibilities**: Shows count metrics cards for Students, Subjects, Assignments, and Results, and provides grid buttons for quick shortcuts.
*   **[ui/student_form.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/student_form.py)**
    *   **Base class**: `tk.Frame` (Student Management Panel).
    *   **Responsibilities**: Prompts input forms for student registration (Admission No, Full Name, Age, Gender combobox, Date of Admission).
*   **[ui/subject_form.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/subject_form.py)**
    *   **Base class**: `tk.Frame` (Subject Management Panel).
    *   **Responsibilities**: Allows adding new subjects, editing existing subject names, and deleting subjects. Highlights selected rows inside a table representation.
*   **[ui/subject_assignment_form.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/subject_assignment_form.py)**
    *   **Base class**: `tk.Frame` (Subject Assignment Panel).
    *   **Responsibilities**: Shows side-by-side listboxes mapping available and assigned subjects. Moving selections updates mapping assignments inside the database junction table.
*   **[ui/result_form.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/result_form.py)**
    *   **Base class**: `tk.Frame` (Result Management Panel).
    *   **Responsibilities**: Grids input forms for assessment/exam marks and displays read-only total marks calculation. Shows recorded scores in a Treeview table along with the student's overall calculated **Mean Score** at the bottom of the table.
*   **[ui/search_view.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/search_view.py)**
    *   **Base class**: `tk.Frame` (Search Panel).
    *   **Responsibilities**: Selects criteria (Name/Admission No) and runs partial directory matching search. Launches the Profile details modal.
*   **[ui/student_profile_view.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/ui/student_profile_view.py)**
    *   **Base class**: `tk.Toplevel` (Popup Detail Window).
    *   **Responsibilities**: Opens details window showing student details, assigned subjects list, and recorded marks.

---

### 6. Utils Directory

*   **[utils/validators.py](file:///c:/Users/sanko/.gemini/antigravity/scratch/student_management_system/utils/validators.py)**
    *   **Purpose**: Validates all inputs before database persistence.
    *   **Key Responsibilities**:
        *   Defapes custom `StudentValidationError` raised on validation failures.
        *   `validate_name(name)`: Verifies names are non-empty.
        *   `validate_age(age)`: Checks that age is an integer between 14 and 20.
        *   `validate_gender(gender)`: Ensures option selected is not default prompt.
        *   `validate_admission_no(no, db_manager, current_id)`: Checks for unique integer admission number.
        *   `validate_admission_date(date)`: Parses date and checks format `YYYY-MM-DD`.
        *   `validate_subject_name(name, db_manager, current_id)`: Verifies unique subject name of length >= 2.
