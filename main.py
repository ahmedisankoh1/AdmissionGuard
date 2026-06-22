from database.db_manager import DatabaseManager
from services.student_service import StudentService
from services.subject_service import SubjectService
from services.assignment_service import AssignmentService
from services.result_service import ResultService
from services.search_service import SearchService
from services.auth_service import AuthService
from ui.main_window import MainWindow

def main():
    # 1. Initialize the database manager (creates db and tables automatically)
    db_manager = DatabaseManager("student_system.db")
    
    # 2. Initialize all service layers
    student_service = StudentService(db_manager)
    subject_service = SubjectService(db_manager)
    assignment_service = AssignmentService(db_manager)
    result_service = ResultService(db_manager)
    search_service = SearchService(db_manager)
    auth_service = AuthService(db_manager)
    
    # 3. Create the MainWindow navigation hub with all services
    print("Launching Student Management System Hub...")
    app = MainWindow(student_service, subject_service, assignment_service, result_service, search_service, auth_service)
    
    # 4. Start the event mainloop
    app.mainloop()
    print("Application closed.")

if __name__ == "__main__":
    main()
