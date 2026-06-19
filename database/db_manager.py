import sqlite3
import os

class DatabaseManager:
    """
    Manages database connections, creates tables, and provides CRUD helper methods.
    """

    def __init__(self, db_path="student_system.db"):
        # Set database path
        self.db_path = os.path.abspath(db_path)
        
        # Create folder if it does not exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        # Automatically create tables
        self.create_tables()

    def get_connection(self):
        # Connect to SQLite database
        conn = sqlite3.connect(self.db_path)
        # Turn on foreign keys constraint checks
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def create_tables(self):
        # Code to create all the database tables
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create students table (admission_no as INTEGER, date_of_admission as DATE)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admission_no INTEGER UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT,
                    date_of_admission DATE NOT NULL
                );
            """)
            
            # Create subjects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_name TEXT UNIQUE NOT NULL,
                    subject_code TEXT UNIQUE NOT NULL
                );
            """)
            
            # Create student_subjects junction table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_subjects (
                    student_id INTEGER NOT NULL,
                    subject_id INTEGER NOT NULL,
                    PRIMARY KEY (student_id, subject_id),
                    FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
                    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
                );
            """)
            
            # Migrate results table if it has the old schema (i.e. 'marks' column exists)
            try:
                cursor.execute("PRAGMA table_info(results);")
                columns = [col[1] for col in cursor.fetchall()]
                if columns and "marks" in columns:
                    print("Old 'results' table schema detected. Dropping table for recreation...")
                    cursor.execute("DROP TABLE results;")
            except sqlite3.Error as migration_error:
                print("Error during results migration check:", migration_error)

            # Create results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    subject_id INTEGER NOT NULL,
                    assessment_mark REAL NOT NULL,
                    exam_mark REAL NOT NULL,
                    total_mark REAL NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
                    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
                );
            """)
            
            conn.commit()
            print("Database initialized and tables created successfully.")
            conn.close()
        except sqlite3.Error as e:
            print("Error creating tables:", e)

    # Reusable method to execute INSERT, UPDATE, DELETE queries
    def execute_query(self, sql, params=()):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            
            # Return last inserted row ID for inserts
            last_id = cursor.lastrowid
            row_count = cursor.rowcount
            
            if last_id is not None and last_id != 0:
                return last_id
            return row_count
        except sqlite3.Error as e:
            print("SQL execution error:", e)
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    # Reusable method to fetch all results of a query
    def fetch_all(self, sql, params=()):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print("SQL fetch all error:", e)
            raise e
        finally:
            if conn:
                conn.close()

    # Reusable method to fetch one result of a query
    def fetch_one(self, sql, params=()):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return row
        except sqlite3.Error as e:
            print("SQL fetch one error:", e)
            raise e
        finally:
            if conn:
                conn.close()
