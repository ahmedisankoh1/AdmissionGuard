import tkinter as tk
from ui.student_form import StudentForm
from ui.subject_form import SubjectForm
from ui.subject_assignment_form import SubjectAssignmentForm
from ui.result_form import ResultForm

class MainWindow(tk.Tk):
    """
    Main Navigation Hub of the Student Management System.
    Provides a dark theme interface to open Student, Subject, and Assignment modules.
    """

    def __init__(self, student_service, subject_service, assignment_service, result_service):
        super().__init__()
        self.student_service = student_service
        self.subject_service = subject_service
        self.assignment_service = assignment_service
        self.result_service = result_service
        
        # Window configurations (increase height to fit 4 buttons)
        self.title("Student Management System")
        self.geometry("400x460")
        self.resizable(False, False)
        
        # Colors
        self.bg_color = "#1e1e2e"
        self.card_color = "#252538"
        self.primary_color = "#74c7ec"   # Title light blue
        self.student_color = "#a6e3a1"   # Green for student manage
        self.subject_color = "#cba6f7"   # Purple for subject manage
        self.assign_color = "#f9e2af"    # Yellow/Amber for assignment manage
        self.text_color = "#f8f8f2"
        
        self.configure(bg=self.bg_color)
        
        # Build UI widgets
        self.create_widgets()

    def create_widgets(self):
        # Application Header Title
        title_label = tk.Label(
            self,
            text="SMS Navigation Hub",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=(25, 10))
        
        # Subtitle message
        subtitle_label = tk.Label(
            self,
            text="Choose a management module to open:",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Button Container Card
        container = tk.Frame(self, bg=self.card_color, padx=25, pady=25)
        container.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        # 1. Manage Students Button
        btn_students = tk.Button(
            container,
            text="Manage Students",
            font=("Segoe UI", 11, "bold"),
            bg=self.student_color,
            fg=self.bg_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#b4befe",
            command=self.open_student_manager
        )
        btn_students.pack(fill="x", ipady=8, pady=(0, 12))
        
        # 2. Manage Subjects Button
        btn_subjects = tk.Button(
            container,
            text="Manage Subjects",
            font=("Segoe UI", 11, "bold"),
            bg=self.subject_color,
            fg=self.bg_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#f5c2e7",
            command=self.open_subject_manager
        )
        btn_subjects.pack(fill="x", ipady=8, pady=(0, 12))
        
        # 3. Subject Assignment Button
        btn_assign = tk.Button(
            container,
            text="Subject Assignment",
            font=("Segoe UI", 11, "bold"),
            bg=self.assign_color,
            fg=self.bg_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#e0af68",
            command=self.open_assignment_manager
        )
        btn_assign.pack(fill="x", ipady=8, pady=(0, 12))

        # 4. Result Management Button
        btn_results = tk.Button(
            container,
            text="Manage Results",
            font=("Segoe UI", 11, "bold"),
            bg=self.primary_color,
            fg=self.bg_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#89b4fa",
            command=self.open_result_manager
        )
        btn_results.pack(fill="x", ipady=8)

    def open_student_manager(self):
        # Open StudentForm in a TopLevel window
        StudentForm(self, self.student_service)

    def open_subject_manager(self):
        # Open SubjectForm in a TopLevel window
        SubjectForm(self, self.subject_service)

    def open_assignment_manager(self):
        # Open SubjectAssignmentForm in a TopLevel window
        SubjectAssignmentForm(self, self.student_service, self.assignment_service)

    def open_result_manager(self):
        # Open ResultForm in a TopLevel window
        ResultForm(self, self.student_service, self.assignment_service, self.result_service)
