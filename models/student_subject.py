class StudentSubject:
    """
    Represents the mapping between a Student and a Subject (junction table).
    """

    def __init__(self, student_id, subject_id, id=None):
        self.student_id = student_id
        self.subject_id = subject_id
        
        # If no id is provided, treat the composite key tuple as the id
        if id is None:
            self.id = (student_id, subject_id)
        else:
            self.id = id

    def assign_subject(self, db_manager):
        # Insert a mapping row into the junction table
        query = "INSERT INTO student_subjects (student_id, subject_id) VALUES (?, ?);"
        params = (self.student_id, self.subject_id)
        
        db_manager.execute_query(query, params)
        return True

    def remove_subject(self, db_manager):
        # Delete the mapping row from the junction table
        query = "DELETE FROM student_subjects WHERE student_id = ? AND subject_id = ?;"
        params = (self.student_id, self.subject_id)
        
        rows_affected = db_manager.execute_query(query, params)
        return rows_affected > 0

    @staticmethod
    def get_student_subjects(db_manager, student_id):
        # Fetch all subject mappings for a given student
        query = "SELECT * FROM student_subjects WHERE student_id = ?;"
        rows = db_manager.fetch_all(query, (student_id,))
        
        assignments = []
        for r in rows:
            # r[0] is student_id, r[1] is subject_id
            assignments.append(StudentSubject(student_id=r[0], subject_id=r[1]))
            
        return assignments

    def __repr__(self):
        return f"StudentSubject(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id})"
