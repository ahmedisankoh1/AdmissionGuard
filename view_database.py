import sqlite3
import os

def view_data():
    db_file = "student_system.db"
    
    # Check if the database file exists
    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' not found.")
        print("Please make sure you have run main.py and saved at least one record.")
        return
        
    print(f"Opening database: {db_file}")
    print("==================================================")
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 1. Fetch Students
        print(" STUDENTS TABLE ")
        print("--------------------------------------------------")
        cursor.execute("SELECT * FROM students;")
        rows = cursor.fetchall()
        
        if len(rows) == 0:
            print("The 'students' table is currently empty.")
        else:
            print(f"Found {len(rows)} student records:\n")
            for row in rows:
                print(f"ID: {row[0]}")
                print(f"Admission No: {row[1]}")
                print(f"Full Name: {row[2]}")
                print(f"Age: {row[3]}")
                print(f"Gender: {row[4]}")
                print(f"Date Admitted: {row[5]}")
                print("-" * 30)
                
        print("\n==================================================")
        
        # 2. Fetch Subjects
        print(" SUBJECTS TABLE ")
        print("--------------------------------------------------")
        cursor.execute("SELECT * FROM subjects;")
        sub_rows = cursor.fetchall()
        
        if len(sub_rows) == 0:
            print("The 'subjects' table is currently empty.")
        else:
            print(f"Found {len(sub_rows)} subject records:\n")
            for row in sub_rows:
                print(f"Subject ID: {row[0]}")
                print(f"Subject Name: {row[1]}")
                print(f"Subject Code: {row[2]}")
                print("-" * 30)
                
        print("\n==================================================")
        
        # 3. Fetch Student-Subject Assignments
        print(" STUDENT-SUBJECT ASSIGNMENTS ")
        print("--------------------------------------------------")
        cursor.execute("""
            SELECT ss.student_id, st.full_name, ss.subject_id, su.subject_name
            FROM student_subjects ss
            INNER JOIN students st ON st.student_id = ss.student_id
            INNER JOIN subjects su ON su.subject_id = ss.subject_id
            ORDER BY ss.student_id ASC;
        """)
        assign_rows = cursor.fetchall()
        
        if len(assign_rows) == 0:
            print("No subject assignments found.")
        else:
            print(f"Found {len(assign_rows)} assignment records:\n")
            for row in assign_rows:
                print(f"Student ID: {row[0]} | Student: {row[1]} | Subject ID: {row[2]} | Subject: {row[3]}")
                
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error occurred:", e)

if __name__ == "__main__":
    view_data()
