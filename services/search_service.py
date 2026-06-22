import sqlite3
from models.student import Student
from utils.validators import StudentValidationError

class SearchService:
    """
    SearchService provides search functions and detailed profiles of students, 
    assigned subjects, and registered results from the database.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def search_by_admission_no(self, admission_no):
        """
        Searches students by admission number using exact/partial matching.
        """
        if not admission_no or str(admission_no).strip() == "":
            raise StudentValidationError("Admission number is required for search.")

        search_term = f"%{str(admission_no).strip()}%"
        query = """
            SELECT student_id, admission_no, full_name, age, gender, date_of_admission 
            FROM students 
            WHERE admission_no LIKE ?
            ORDER BY admission_no ASC;
        """
        try:
            rows = self.db_manager.fetch_all(query, (search_term,))
            students = []
            for r in rows:
                students.append(Student(
                    student_id=r[0],
                    admission_no=r[1],
                    full_name=r[2],
                    age=r[3],
                    gender=r[4],
                    date_of_admission=r[5]
                ))
            return students
        except sqlite3.Error as e:
            raise Exception(f"Database query failed: {e}")

    def search_by_name(self, name):
        """
        Searches students by name using partial matching.
        """
        if not name or name.strip() == "":
            raise StudentValidationError("Student name is required for search.")

        search_term = f"%{name.strip()}%"
        query = """
            SELECT student_id, admission_no, full_name, age, gender, date_of_admission 
            FROM students 
            WHERE full_name LIKE ?
            ORDER BY full_name ASC;
        """
        try:
            rows = self.db_manager.fetch_all(query, (search_term,))
            students = []
            for r in rows:
                students.append(Student(
                    student_id=r[0],
                    admission_no=r[1],
                    full_name=r[2],
                    age=r[3],
                    gender=r[4],
                    date_of_admission=r[5]
                ))
            return students
        except sqlite3.Error as e:
            raise Exception(f"Database query failed: {e}")

    def get_student_profile(self, student_id):
        """
        Fetches student details by ID.
        """
        query = """
            SELECT student_id, admission_no, full_name, age, gender, date_of_admission 
            FROM students 
            WHERE student_id = ?;
        """
        try:
            row = self.db_manager.fetch_one(query, (student_id,))
            if row is None:
                return None
            return Student(
                student_id=row[0],
                admission_no=row[1],
                full_name=row[2],
                age=row[3],
                gender=row[4],
                date_of_admission=row[5]
            )
        except sqlite3.Error as e:
            raise Exception(f"Database fetch failed: {e}")

    def get_student_subjects(self, student_id):
        """
        Fetches all subjects assigned to a student.
        """
        query = """
            SELECT s.subject_id, s.subject_name, s.subject_code 
            FROM subjects s
            INNER JOIN student_subjects ss ON s.subject_id = ss.subject_id
            WHERE ss.student_id = ?
            ORDER BY s.subject_name ASC;
        """
        try:
            rows = self.db_manager.fetch_all(query, (student_id,))
            subjects = []
            for r in rows:
                subjects.append({
                    "subject_id": r[0],
                    "subject_name": r[1],
                    "subject_code": r[2]
                })
            return subjects
        except sqlite3.Error as e:
            raise Exception(f"Database fetch failed: {e}")

    def get_student_results(self, student_id):
        """
        Fetches all recorded results for a student.
        """
        query = """
            SELECT s.subject_name, s.subject_code, r.assessment_mark, r.exam_mark, r.total_mark
            FROM results r
            INNER JOIN subjects s ON r.subject_id = s.subject_id
            WHERE r.student_id = ?
            ORDER BY s.subject_name ASC;
        """
        try:
            rows = self.db_manager.fetch_all(query, (student_id,))
            results = []
            for r in rows:
                results.append({
                    "subject_name": r[0],
                    "subject_code": r[1],
                    "assessment_mark": r[2],
                    "exam_mark": r[3],
                    "total_mark": r[4]
                })
            return results
        except sqlite3.Error as e:
            raise Exception(f"Database fetch failed: {e}")

    def calculate_student_mean(self, student_id):
        """
        Calculates the mean score for a student based on all recorded subjects.
        Returns the float mean value, or None if no results exist.
        """
        query = "SELECT total_mark FROM results WHERE student_id = ?;"
        try:
            rows = self.db_manager.fetch_all(query, (student_id,))
            if not rows:
                return None
            total_sum = sum(r[0] for r in rows)
            count = len(rows)
            return total_sum / count
        except sqlite3.Error as e:
            raise Exception(f"Database query failed during mean calculation: {e}")
