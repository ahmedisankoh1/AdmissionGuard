class Result:
    """
    Represents a student's result for a subject and handles database CRUD operations.
    """

    def __init__(self, student_id, subject_id, assessment_mark, exam_mark, total_mark=None, result_id=None):
        self.result_id = result_id
        self.student_id = student_id
        self.subject_id = subject_id
        self.assessment_mark = float(assessment_mark) if assessment_mark is not None else 0.0
        self.exam_mark = float(exam_mark) if exam_mark is not None else 0.0
        
        # Calculate total_mark if not provided
        if total_mark is None:
            self.calculate_total()
        else:
            self.total_mark = float(total_mark)

    def calculate_total(self):
        """
        Calculates and updates total_mark as the sum of assessment_mark and exam_mark.
        """
        self.total_mark = self.assessment_mark + self.exam_mark
        return self.total_mark

    def save_result(self, db_manager):
        """
        Saves a new result entry to the database and returns the generated result_id.
        """
        self.calculate_total()
        query = """
            INSERT INTO results (student_id, subject_id, assessment_mark, exam_mark, total_mark)
            VALUES (?, ?, ?, ?, ?);
        """
        params = (self.student_id, self.subject_id, self.assessment_mark, self.exam_mark, self.total_mark)
        self.result_id = db_manager.execute_query(query, params)
        return self.result_id

    def update_result(self, db_manager):
        """
        Updates the marks for an existing result in the database.
        """
        self.calculate_total()
        query = """
            UPDATE results 
            SET assessment_mark = ?, exam_mark = ?, total_mark = ? 
            WHERE result_id = ?;
        """
        params = (self.assessment_mark, self.exam_mark, self.total_mark, self.result_id)
        rows_affected = db_manager.execute_query(query, params)
        return rows_affected > 0

    @staticmethod
    def get_results(db_manager, student_id=None):
        """
        Retrieves all results, or filters results for a specific student_id.
        """
        if student_id is not None:
            query = "SELECT * FROM results WHERE student_id = ? ORDER BY result_id ASC;"
            rows = db_manager.fetch_all(query, (student_id,))
        else:
            query = "SELECT * FROM results ORDER BY result_id ASC;"
            rows = db_manager.fetch_all(query)
            
        results_list = []
        for r in rows:
            results_list.append(Result(
                result_id=r[0],
                student_id=r[1],
                subject_id=r[2],
                assessment_mark=r[3],
                exam_mark=r[4],
                total_mark=r[5]
            ))
        return results_list

    def __repr__(self):
        return f"Result({self.result_id}, Student: {self.student_id}, Subject: {self.subject_id}, Marks: {self.assessment_mark} + {self.exam_mark} = {self.total_mark})"
