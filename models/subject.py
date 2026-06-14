import random

class Subject:
    """
    Represents a subject entity and handles CRUD database operations.
    """

    def __init__(self, subject_name=None, subject_code=None, subject_id=None):
        self.subject_id = subject_id
        self.subject_name = subject_name
        
        # If no subject code is provided, auto-generate one
        if subject_code is None and subject_name is not None:
            self.subject_code = self.generate_code(subject_name)
        else:
            self.subject_code = subject_code

    def generate_code(self, name):
        # Clean the name to letters only and uppercase it
        clean_name = ""
        for char in name:
            if char.isalnum():
                clean_name += char.upper()
                
        # Take up to first 3 characters, pad with 'SUB' if too short
        prefix = clean_name[:3]
        while len(prefix) < 3:
            prefix += "SUB"
            
        # Add a random 3-digit number to make it unique
        random_num = random.randint(100, 999)
        return f"{prefix}-{random_num}"

    def create_subject(self, db_manager):
        # Insert a new subject row into the subjects table
        query = "INSERT INTO subjects (subject_name, subject_code) VALUES (?, ?);"
        params = (self.subject_name, self.subject_code)
        
        # Execute query and assign the auto-incremented subject_id
        self.subject_id = db_manager.execute_query(query, params)
        return self.subject_id

    def update_subject(self, db_manager):
        # Update an existing subject name in the database
        query = "UPDATE subjects SET subject_name = ? WHERE subject_id = ?;"
        params = (self.subject_name, self.subject_id)
        
        rows_affected = db_manager.execute_query(query, params)
        return rows_affected > 0

    def delete_subject(self, db_manager):
        # Delete the subject from the database
        query = "DELETE FROM subjects WHERE subject_id = ?;"
        params = (self.subject_id,)
        
        rows_affected = db_manager.execute_query(query, params)
        return rows_affected > 0

    def __repr__(self):
        return f"Subject({self.subject_id}, '{self.subject_name}', '{self.subject_code}')"
