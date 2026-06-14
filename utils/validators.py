from datetime import datetime, date

class StudentValidationError(Exception):
    """
    Custom exception class to handle student and subject validation errors.
    """
    pass


def validate_name(name):
    # Check if name is empty or just spaces
    if name == "" or name is None or name.strip() == "":
        raise StudentValidationError("Name must not be empty.")
    return name.strip()


def validate_age(age):
    # Try to convert age to an integer
    try:
        age_val = int(age)
    except (TypeError, ValueError):
        raise StudentValidationError("Age must be a valid integer.")
        
    # Check if age is between 14 and 20
    if age_val < 14 or age_val > 20:
        raise StudentValidationError("Age must be between 14 and 20.")
        
    return age_val


def validate_gender(gender):
    # Check if gender is empty, None, or default prompt value
    if gender == "" or gender is None or gender.strip() == "" or gender.strip() == "Select Gender":
        raise StudentValidationError("Gender is required.")
    return gender.strip()


def validate_admission_no(admission_no, db_manager=None, current_student_id=None):
    # Check if admission number is empty
    if admission_no == "" or admission_no is None or str(admission_no).strip() == "":
        raise StudentValidationError("Admission Number must not be empty.")
        
    # Check if admission number is a valid integer
    try:
        admission_int = int(admission_no)
    except (TypeError, ValueError):
        raise StudentValidationError("Admission Number must be an integer (digits only).")
    
    # Check if this admission number is unique in the database
    if db_manager is not None:
        if current_student_id is not None:
            # We are updating, so ignore the student's own record
            query = "SELECT COUNT(*) FROM students WHERE admission_no = ? AND student_id != ?"
            result = db_manager.fetch_one(query, (admission_int, current_student_id))
        else:
            # We are registering a new student
            query = "SELECT COUNT(*) FROM students WHERE admission_no = ?"
            result = db_manager.fetch_one(query, (admission_int,))
            
        # If count is greater than 0, then it's a duplicate
        if result is not None and result[0] > 0:
            raise StudentValidationError(f"Admission Number '{admission_int}' is already in use.")
            
    return admission_int


def validate_admission_date(date_val):
    # Check if the date is empty
    if date_val is None:
        raise StudentValidationError("Date of Admission must not be empty.")
        
    # If it is already a date object, it is valid
    if isinstance(date_val, date):
        return date_val
        
    # If it is a string, check if it's empty and parse it
    if isinstance(date_val, str):
        stripped_date = date_val.strip()
        if stripped_date == "":
            raise StudentValidationError("Date of Admission must not be empty.")
        try:
            # Parse YYYY-MM-DD string into a date object
            parsed_date = datetime.strptime(stripped_date, "%Y-%m-%d").date()
            return parsed_date
        except ValueError:
            raise StudentValidationError("Date of Admission must be in YYYY-MM-DD format.")
            
    raise StudentValidationError("Invalid date type.")


def validate_subject_name(subject_name, db_manager=None, current_subject_id=None):
    # Check if subject name is empty or just spaces
    if subject_name == "" or subject_name is None or subject_name.strip() == "":
        raise StudentValidationError("Subject Name must not be empty.")
        
    subject_name = subject_name.strip()
    
    # Check minimum length (must be at least 2 characters)
    if len(subject_name) < 2:
        raise StudentValidationError("Subject Name must be at least 2 characters long.")
        
    # Check if subject name is unique
    if db_manager is not None:
        if current_subject_id is not None:
            query = "SELECT COUNT(*) FROM subjects WHERE subject_name = ? AND subject_id != ?"
            result = db_manager.fetch_one(query, (subject_name, current_subject_id))
        else:
            query = "SELECT COUNT(*) FROM subjects WHERE subject_name = ?"
            result = db_manager.fetch_one(query, (subject_name,))
            
        if result is not None and result[0] > 0:
            raise StudentValidationError(f"Subject '{subject_name}' already exists.")
            
    return subject_name
