from models.student import Student

class StudentService:
    """
    StudentService acts as the intermediary (Service Layer) between the UI layer
    and the Student Model / Database Manager.
    """

    def __init__(self, db_manager):
        # Service needs db_manager to save and retrieve data
        self.db_manager = db_manager

    def create_student(self, admission_no, full_name, age, gender, date_of_admission):
        # Instantiate a new Student object
        new_student = Student(
            admission_no=admission_no,
            full_name=full_name,
            age=age,
            gender=gender,
            date_of_admission=date_of_admission
        )
        
        # Register the student in the database (calls validation inside register_student)
        new_student.register_student(self.db_manager)
        return new_student

    def get_student(self, student_id):
        # Fetch a single student by ID
        return Student.get_by_id(self.db_manager, student_id)

    def get_all_students(self):
        # Fetch all students in the system
        # Running search_student with empty string returns all students (since LIKE '%%' matches everything)
        return Student.search_student(self.db_manager, "")
