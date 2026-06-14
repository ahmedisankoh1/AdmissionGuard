from models.subject import Subject
from utils.validators import validate_subject_name, StudentValidationError

class SubjectService:
    """
    SubjectService acts as the intermediary (Service Layer) between the UI layer
    and the Subject Model / Database Manager.
    Handles business validations, CRUD execution, and errors.
    """

    def __init__(self, db_manager):
        # Requires database manager to run queries
        self.db_manager = db_manager

    def create_subject(self, name):
        # 1. Validate the subject name
        validated_name = validate_subject_name(name, self.db_manager)
        
        # 2. Instantiate the Subject model (will auto-generate course code)
        subject = Subject(subject_name=validated_name)
        
        # 3. Save to database
        subject.create_subject(self.db_manager)
        return subject

    def update_subject(self, subject_id, new_name):
        # 1. Validate the new name (ignoring self-collision on uniqueness check)
        validated_name = validate_subject_name(new_name, self.db_manager, subject_id)
        
        # 2. Instantiate Subject with target ID and new name
        subject = Subject(subject_id=subject_id, subject_name=validated_name)
        
        # 3. Update database
        success = subject.update_subject(self.db_manager)
        return success

    def delete_subject(self, subject_id):
        # 1. Instantiate Subject model with target ID
        subject = Subject(subject_id=subject_id)
        
        # 2. Execute deletion
        success = subject.delete_subject(self.db_manager)
        return success

    def get_all_subjects(self):
        # 1. Query all subjects
        query = "SELECT * FROM subjects ORDER BY subject_id ASC;"
        rows = self.db_manager.fetch_all(query)
        
        # 2. Convert database rows into Subject objects
        subjects_list = []
        for r in rows:
            sub = Subject(
                subject_id=r[0],
                subject_name=r[1],
                subject_code=r[2]
            )
            subjects_list.append(sub)
            
        return subjects_list
