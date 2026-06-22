import tkinter as tk
from tkinter import messagebox
from ui.dashboard_view import DashboardView
from ui.student_form import StudentForm
from ui.subject_form import SubjectForm
from ui.subject_assignment_form import SubjectAssignmentForm
from ui.result_form import ResultForm
from ui.search_view import SearchView

class MainWindow(tk.Tk):
    """
    Main Navigation Hub of the Student Management System.
    Refactored to implement a modern single-window layout with a persistent sidebar.
    """

    def __init__(self, student_service, subject_service, assignment_service, result_service, search_service, auth_service):
        super().__init__()
        self.student_service = student_service
        self.subject_service = subject_service
        self.assignment_service = assignment_service
        self.result_service = result_service
        self.search_service = search_service
        self.auth_service = auth_service
        
        # Hide main window initially during login phase
        self.withdraw()
        
        # Window configurations (Large landscape dashboard window)
        self.title("Admission Guard - Student Management System")
        self.geometry("1024x680")
        self.resizable(True, True)
        self.minimum_size = (900, 600)
        self.minsize(900, 600)
        
        # Color palette (Professional Education theme)
        self.bg_color = "#F8FAFC"        # Background (slate gray)
        self.sidebar_color = "#1E293B"   # Sidebar (dark slate)
        self.text_primary = "#111827"
        self.text_light = "#FFFFFF"
        self.primary_color = "#1E3A8A"   # Deep Blue
        self.secondary_color = "#3B82F6" # Bright Blue (Active Tab Accent)
        self.accent_color = "#EF4444"    # Red (Logout hover)
        
        self.configure(bg=self.bg_color)
        
        # Track active navigation elements
        self.current_frame = None
        self.nav_buttons = {}
        
        # Build UI widgets (sidebar and content area)
        self.create_widgets()
        
        # Launch login window
        self.open_login_screen()

    def create_widgets(self):
        # 1. Persistent Sidebar Frame (Left)
        self.sidebar = tk.Frame(self, bg=self.sidebar_color, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Prevent sidebar resizing to fit buttons
        
        # Sidebar Logo area
        logo_container = tk.Frame(self.sidebar, bg=self.sidebar_color, pady=25)
        logo_container.pack(fill="x")
        
        lbl_logo = tk.Label(
            logo_container, text="Admission Guard",
            font=("Segoe UI", 14, "bold"), bg=self.sidebar_color, fg=self.text_light
        )
        lbl_logo.pack(fill="x")
        
        lbl_sub = tk.Label(
            logo_container, text="Student Manager System",
            font=("Segoe UI", 8), bg=self.sidebar_color, fg="#94A3B8"
        )
        lbl_sub.pack(fill="x")

        # Divider line
        divider = tk.Frame(self.sidebar, bg="#334155", height=1)
        divider.pack(fill="x", padx=15, pady=(0, 15))

        # Sidebar navigation buttons definitions
        tabs = [
            ("Dashboard", "Dashboard"),
            ("Students", "Students"),
            ("Subjects", "Subjects"),
            ("Assignments", "Assignments"),
            ("Results", "Results"),
            ("Search Directory", "Search")
        ]

        for label, target in tabs:
            btn = tk.Button(
                self.sidebar, text=f"  {label}", font=("Segoe UI", 10, "bold"),
                bg=self.sidebar_color, fg="#94A3B8", relief="flat", bd=0, anchor="w",
                cursor="hand2", activebackground="#334155", activeforeground=self.text_light,
                command=lambda t=target: self.switch_to_tab(t)
            )
            btn.pack(fill="x", ipady=10, padx=10, pady=2)
            self.nav_buttons[target] = btn
            
            # Hover bindings
            btn.bind("<Enter>", lambda e, b=btn: self.on_sidebar_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.on_sidebar_hover(b, False))

        # Logout button anchored at the bottom
        self.btn_logout = tk.Button(
            self.sidebar, text="  Logout", font=("Segoe UI", 10, "bold"),
            bg=self.sidebar_color, fg="#EF4444", relief="flat", bd=0, anchor="w",
            cursor="hand2", activebackground="#EF4444", activeforeground=self.text_light,
            command=self.on_logout
        )
        self.btn_logout.pack(side="bottom", fill="x", ipady=10, padx=10, pady=15)
        self.btn_logout.bind("<Enter>", lambda e: self.btn_logout.config(bg="#EF4444", fg=self.text_light))
        self.btn_logout.bind("<Leave>", lambda e: self.btn_logout.config(bg=self.sidebar_color, fg="#EF4444"))

        # 2. Main Content Frame (Right)
        self.content_container = tk.Frame(self, bg=self.bg_color)
        self.content_container.pack(side="right", fill="both", expand=True)

    def on_sidebar_hover(self, btn, is_hover):
        # Ignore hover effect if the button is currently the active tab
        for target, active_btn in self.nav_buttons.items():
            if active_btn == btn and btn.cget("bg") == self.secondary_color:
                return
                
        if is_hover:
            btn.config(bg="#334155", fg=self.text_light)
        else:
            btn.config(bg=self.sidebar_color, fg="#94A3B8")

    def switch_to_tab(self, tab_name):
        """
        Switches the main content frame to display the chosen module/view.
        """
        # Destroy the currently active view frame
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        # Highlight active sidebar tab
        for target, btn in self.nav_buttons.items():
            if target == tab_name:
                btn.config(bg=self.secondary_color, fg=self.text_light)
            else:
                btn.config(bg=self.sidebar_color, fg="#94A3B8")

        # Instantiate the correct frame class inside content container
        if tab_name == "Dashboard":
            self.current_frame = DashboardView(
                self.content_container,
                db_manager=self.student_service.db_manager,
                nav_callback=self.switch_to_tab
            )
        elif tab_name == "Students":
            self.current_frame = StudentForm(self.content_container, self.student_service)
        elif tab_name == "Subjects":
            self.current_frame = SubjectForm(self.content_container, self.subject_service)
        elif tab_name == "Assignments":
            self.current_frame = SubjectAssignmentForm(self.content_container, self.student_service, self.assignment_service)
        elif tab_name == "Results":
            self.current_frame = ResultForm(self.content_container, self.student_service, self.assignment_service, self.result_service)
        elif tab_name == "Search":
            self.current_frame = SearchView(self.content_container, self.search_service)
            
        # Pack the new active view frame to fill the content container
        self.current_frame.pack(fill="both", expand=True)

    def open_login_screen(self):
        from ui.login_form import LoginForm
        # Create login form as Toplevel modal popup
        login_window = LoginForm(self, self.auth_service, self.on_login_success)
        # Handle case where user closes the login window: exit application
        login_window.protocol("WM_DELETE_WINDOW", self.on_login_cancel)

    def on_login_success(self):
        # Refresh dashboard metrics, load default view, and deiconify
        self.switch_to_tab("Dashboard")
        self.deiconify()  # Show MainWindow

    def on_login_cancel(self):
        self.destroy()  # Exit the application if login is cancelled/closed

    def on_logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if confirm:
            self.auth_service.logout()
            self.withdraw() # Hide MainWindow
            self.open_login_screen()
