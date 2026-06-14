from utils.validators import validate_name, validate_age, validate_admission_no, validate_gender, validate_admission_date, StudentValidationError
from datetime import datetime, date

class Student:
    """
    Represents a student entity and handles registration, updates, and searches.
    """

    def __init__(self, admission_no, full_name, age, gender, date_of_admission=None, student_id=None):
        self.student_id = student_id
        
        # Try to parse admission_no as integer if possible
        try:
            self.admission_no = int(admission_no) if admission_no is not None else None
        except ValueError:
            # Leave it as string so validator catches the type error
            self.admission_no = admission_no
            
        self.full_name = full_name
        self.age = age
        self.gender = gender
        
        # Store date_of_admission as a Python date object
        if date_of_admission is None:
            self.date_of_admission = date.today()
        elif isinstance(date_of_admission, str):
            try:
                # Try parsing the string to a date object
                self.date_of_admission = datetime.strptime(date_of_admission.strip(), "%Y-%m-%d").date()
            except ValueError:
                # Keep original string if invalid to let validator throw error
                self.date_of_admission = date_of_admission
        else:
            self.date_of_admission = date_of_admission

    def register_student(self, db_manager):
        # Prevent registering if student already has a student_id
        if self.student_id is not None:
            raise StudentValidationError("Student is already registered (already has student_id).")

        # Run all validation rules (raises exceptions if invalid)
        self.full_name = validate_name(self.full_name)
        self.age = validate_age(self.age)
        self.gender = validate_gender(self.gender)
        self.admission_no = validate_admission_no(self.admission_no, db_manager)
        self.date_of_admission = validate_admission_date(self.date_of_admission)

        # SQL insert query (date stored as string 'YYYY-MM-DD' in SQLite)
        query = "INSERT INTO students (admission_no, full_name, age, gender, date_of_admission) VALUES (?, ?, ?, ?, ?);"
        params = (self.admission_no, self.full_name, self.age, self.gender, str(self.date_of_admission))
        
        # Execute query and save the assigned ID
        self.student_id = db_manager.execute_query(query, params)
        return self.student_id

    def update_student(self, db_manager):
        # Make sure student is already registered
        if self.student_id is None:
            raise StudentValidationError("Cannot update student without a student_id.")

        # Validate inputs (passing current student_id to avoid duplicate checks with itself)
        self.full_name = validate_name(self.full_name)
        self.age = validate_age(self.age)
        self.gender = validate_gender(self.gender)
        self.admission_no = validate_admission_no(self.admission_no, db_manager, self.student_id)
        self.date_of_admission = validate_admission_date(self.date_of_admission)

        # SQL update query
        query = "UPDATE students SET admission_no = ?, full_name = ?, age = ?, gender = ?, date_of_admission = ? WHERE student_id = ?;"
        params = (self.admission_no, self.full_name, self.age, self.gender, str(self.date_of_admission), self.student_id)
        
        rows_affected = db_manager.execute_query(query, params)
        if rows_affected > 0:
            return True
        return False

    @staticmethod
    def search_student(db_manager, search_term):
        # Search student by name or admission number using LIKE
        query = "SELECT * FROM students WHERE full_name LIKE ? OR admission_no LIKE ?;"
        like_pattern = "%" + search_term + "%"
        
        rows = db_manager.fetch_all(query, (like_pattern, like_pattern))
        
        # Build Student objects from query results
        student_list = []
        for r in rows:
            student = Student(
                student_id=r[0],
                admission_no=r[1],
                full_name=r[2],
                age=r[3],
                gender=r[4],
                date_of_admission=r[5]
            )
            student_list.append(student)
            
        return student_list

    @staticmethod
    def get_by_id(db_manager, student_id):
        # Get a single student by id
        query = "SELECT * FROM students WHERE student_id = ?;"
        r = db_manager.fetch_one(query, (student_id,))
        if r is not None:
            return Student(
                student_id=r[0],
                admission_no=r[1],
                full_name=r[2],
                age=r[3],
                gender=r[4],
                date_of_admission=r[5]
            )
        return None

    def __repr__(self):
        return f"Student({self.student_id}, {self.admission_no}, '{self.full_name}', {self.age}, '{self.gender}', '{self.date_of_admission}')"
