from models.student_subject import StudentSubject
from models.subject import Subject
from utils.validators import StudentValidationError

class AssignmentService:
    """
    AssignmentService coordinates subject mapping, duplicate checks,
    and the 8-subject maximum validation limit.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def assign_subject_to_student(self, student_id, subject_id):
        # 1. Validate that the student exists
        student_query = "SELECT COUNT(*) FROM students WHERE student_id = ?;"
        student_check = self.db_manager.fetch_one(student_query, (student_id,))
        if student_check is None or student_check[0] == 0:
            raise StudentValidationError("Student does not exist.")
            
        # 2. Validate that the subject exists
        subject_query = "SELECT COUNT(*) FROM subjects WHERE subject_id = ?;"
        subject_check = self.db_manager.fetch_one(subject_query, (subject_id,))
        if subject_check is None or subject_check[0] == 0:
            raise StudentValidationError("Subject does not exist.")
            
        # 3. Prevent duplicate assignments (assigned twice)
        dup_query = "SELECT COUNT(*) FROM student_subjects WHERE student_id = ? AND subject_id = ?;"
        dup_check = self.db_manager.fetch_one(dup_query, (student_id, subject_id))
        if dup_check is not None and dup_check[0] > 0:
            raise StudentValidationError("Subject is already assigned to this student.")
            
        # 4. Limit to a maximum of 8 subjects
        limit_query = "SELECT COUNT(*) FROM student_subjects WHERE student_id = ?;"
        limit_check = self.db_manager.fetch_one(limit_query, (student_id,))
        if limit_check is not None and limit_check[0] >= 8:
            raise StudentValidationError("Student has reached the maximum limit of 8 assigned subjects.")
            
        # 5. Create mapping object and execute database insert
        mapping = StudentSubject(student_id=student_id, subject_id=subject_id)
        return mapping.assign_subject(self.db_manager)

    def remove_subject_from_student(self, student_id, subject_id):
        # Create mapping object and execute deletion
        mapping = StudentSubject(student_id=student_id, subject_id=subject_id)
        return mapping.remove_subject(self.db_manager)

    def get_assigned_subjects(self, student_id):
        # Fetch all subjects mapped to a student (INNER JOIN)
        query = """
            SELECT s.subject_id, s.subject_name, s.subject_code 
            FROM subjects s
            INNER JOIN student_subjects ss ON s.subject_id = ss.subject_id
            WHERE ss.student_id = ?
            ORDER BY s.subject_id ASC;
        """
        rows = self.db_manager.fetch_all(query, (student_id,))
        
        assigned_list = []
        for r in rows:
            sub = Subject(
                subject_id=r[0],
                subject_name=r[1],
                subject_code=r[2]
            )
            assigned_list.append(sub)
            
        return assigned_list

    def get_available_subjects(self, student_id):
        # Fetch all subjects NOT currently mapped to a student (subquery NOT IN)
        query = """
            SELECT s.subject_id, s.subject_name, s.subject_code 
            FROM subjects s
            WHERE s.subject_id NOT IN (
                SELECT ss.subject_id FROM student_subjects ss WHERE ss.student_id = ?
            )
            ORDER BY s.subject_id ASC;
        """
        rows = self.db_manager.fetch_all(query, (student_id,))
        
        available_list = []
        for r in rows:
            sub = Subject(
                subject_id=r[0],
                subject_name=r[1],
                subject_code=r[2]
            )
            available_list.append(sub)
            
        return available_list
