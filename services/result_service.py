from models.result import Result
from utils.validators import StudentValidationError

class ResultService:
    """
    Coordinates result recording, updates, calculations, and validation checks.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def calculate_total(self, assessment_mark, exam_mark):
        """
        Calculates total mark after validating types.
        """
        try:
            am = float(assessment_mark)
            em = float(exam_mark)
        except (ValueError, TypeError):
            raise StudentValidationError("Marks must be valid numbers.")
        return am + em

    def _validate_marks(self, assessment_mark, exam_mark):
        """
        Validation helper for result marks.
        """
        try:
            # Check for empty strings or None
            if assessment_mark is None or str(assessment_mark).strip() == "":
                raise StudentValidationError("Assessment Mark must not be empty.")
            if exam_mark is None or str(exam_mark).strip() == "":
                raise StudentValidationError("Exam Mark must not be empty.")
                
            am = float(assessment_mark)
            em = float(exam_mark)
        except (ValueError, TypeError):
            raise StudentValidationError("Marks must be valid numbers.")

        if am < 0 or am > 30:
            raise StudentValidationError("Assessment Mark must be between 0 and 30.")

        if em < 0 or em > 70:
            raise StudentValidationError("Exam Mark must be between 0 and 70.")

        total = am + em
        if total > 100:
            raise StudentValidationError("Total Mark cannot exceed 100.")

        return am, em, total

    def _validate_assignment(self, student_id, subject_id):
        """
        Ensures a student has been assigned a subject before a result can be saved.
        """
        # Validate that the student exists
        student_query = "SELECT COUNT(*) FROM students WHERE student_id = ?;"
        student_check = self.db_manager.fetch_one(student_query, (student_id,))
        if student_check is None or student_check[0] == 0:
            raise StudentValidationError("Student does not exist.")

        # Validate that the subject exists
        subject_query = "SELECT COUNT(*) FROM subjects WHERE subject_id = ?;"
        subject_check = self.db_manager.fetch_one(subject_query, (subject_id,))
        if subject_check is None or subject_check[0] == 0:
            raise StudentValidationError("Subject does not exist.")

        # Validate assignment
        query = "SELECT COUNT(*) FROM student_subjects WHERE student_id = ? AND subject_id = ?;"
        res = self.db_manager.fetch_one(query, (student_id, subject_id))
        if res is None or res[0] == 0:
            raise StudentValidationError("This subject is not assigned to the selected student.")

    def save_result(self, student_id, subject_id, assessment_mark, exam_mark):
        """
        Saves a student's result for a subject. Prevents duplicates by throwing an error.
        """
        # 1. Validate assignment
        self._validate_assignment(student_id, subject_id)

        # 2. Validate marks
        am, em, total = self._validate_marks(assessment_mark, exam_mark)

        # 3. Check for duplicates
        dup_query = "SELECT COUNT(*) FROM results WHERE student_id = ? AND subject_id = ?;"
        dup_check = self.db_manager.fetch_one(dup_query, (student_id, subject_id))
        if dup_check is not None and dup_check[0] > 0:
            raise StudentValidationError("Result already exists for this subject. Please edit the existing result.")

        # 4. Instantiate Result model and save
        result = Result(
            student_id=student_id,
            subject_id=subject_id,
            assessment_mark=am,
            exam_mark=em,
            total_mark=total
        )
        return result.save_result(self.db_manager)

    def update_result(self, result_id, assessment_mark, exam_mark):
        """
        Updates an existing result record.
        """
        # 1. Check if result exists
        query = "SELECT student_id, subject_id FROM results WHERE result_id = ?;"
        res = self.db_manager.fetch_one(query, (result_id,))
        if res is None:
            raise StudentValidationError("Result record not found.")
        
        student_id, subject_id = res[0], res[1]

        # 2. Verify assignment (in case assignments were removed)
        self._validate_assignment(student_id, subject_id)

        # 3. Validate marks
        am, em, total = self._validate_marks(assessment_mark, exam_mark)

        # 4. Instantiate Result model and update
        result = Result(
            result_id=result_id,
            student_id=student_id,
            subject_id=subject_id,
            assessment_mark=am,
            exam_mark=em,
            total_mark=total
        )
        return result.update_result(self.db_manager)

    def get_student_results(self, student_id):
        """
        Fetches student results with subject names.
        """
        query = """
            SELECT r.result_id, r.student_id, r.subject_id, s.subject_name, s.subject_code, 
                   r.assessment_mark, r.exam_mark, r.total_mark
            FROM results r
            INNER JOIN subjects s ON r.subject_id = s.subject_id
            WHERE r.student_id = ?
            ORDER BY r.result_id ASC;
        """
        rows = self.db_manager.fetch_all(query, (student_id,))
        
        results_list = []
        for r in rows:
            results_list.append({
                "result_id": r[0],
                "student_id": r[1],
                "subject_id": r[2],
                "subject_name": r[3],
                "subject_code": r[4],
                "assessment_mark": r[5],
                "exam_mark": r[6],
                "total_mark": r[7]
            })
        return results_list

    def get_subject_results(self, subject_id):
        """
        Fetches subject results with student names.
        """
        query = """
            SELECT r.result_id, r.student_id, st.full_name, r.subject_id, 
                   r.assessment_mark, r.exam_mark, r.total_mark
            FROM results r
            INNER JOIN students st ON r.student_id = st.student_id
            WHERE r.subject_id = ?
            ORDER BY r.result_id ASC;
        """
        rows = self.db_manager.fetch_all(query, (subject_id,))
        
        results_list = []
        for r in rows:
            results_list.append({
                "result_id": r[0],
                "student_id": r[1],
                "student_name": r[2],
                "subject_id": r[3],
                "assessment_mark": r[4],
                "exam_mark": r[5],
                "total_mark": r[6]
            })
        return results_list

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
        except Exception as e:
            raise Exception(f"Database query failed during mean calculation: {e}")
