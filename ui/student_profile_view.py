import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class StudentProfileView(tk.Toplevel):
    """
    Tkinter Student Profile Window.
    Displays a comprehensive view of a student's personal information,
    assigned subjects, and recorded results.
    """

    def __init__(self, parent, student_id, search_service):
        super().__init__(parent)
        self.student_id = student_id
        self.search_service = search_service

        # Window settings
        self.title("Student Profile")
        self.geometry("680x740")
        self.resizable(False, False)

        # Audit color palette (Professional Education theme)
        self.bg_color = "#F8FAFC"
        self.card_color = "#FFFFFF"
        self.text_primary = "#111827"
        self.text_secondary = "#6B7280"
        self.primary_color = "#1E3A8A"   # Deep Blue (Title)
        self.secondary_color = "#3B82F6" # Bright Blue
        self.success_color = "#10B981"   # Green (Mean Score accent)
        self.accent_color = "#EF4444"    # Red (Close)
        self.entry_bg = "#F8FAFC"
        self.entry_border = "#E2E8F0"

        self.configure(bg=self.bg_color)

        # Build UI
        self.create_widgets()

        # Load Student Data
        self.load_data()

    def create_widgets(self):
        # Header Title
        title_label = tk.Label(
            self,
            text="Student Profile Dashboard",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=(15, 10))

        # --- SECTION 1: Personal Info Card ---
        info_frame = tk.LabelFrame(
            self, text="Student Personal Information", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.primary_color, labelanchor="n", padx=15, pady=15,
            highlightbackground=self.entry_border, highlightthickness=1, bd=0
        )
        info_frame.pack(fill="x", padx=25, pady=5)
        
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=2)
        info_frame.columnconfigure(2, weight=1)
        info_frame.columnconfigure(3, weight=2)

        # Labels for Information
        self.lbl_admission_title = tk.Label(info_frame, text="Admission No:", font=("Segoe UI", 9, "bold"), bg=self.card_color, fg=self.text_primary)
        self.lbl_admission_val = tk.Label(info_frame, text="-", font=("Segoe UI", 9), bg=self.card_color, fg=self.text_secondary, anchor="w")
        
        self.lbl_name_title = tk.Label(info_frame, text="Full Name:", font=("Segoe UI", 9, "bold"), bg=self.card_color, fg=self.text_primary)
        self.lbl_name_val = tk.Label(info_frame, text="-", font=("Segoe UI", 9), bg=self.card_color, fg=self.text_secondary, anchor="w")
        
        self.lbl_age_title = tk.Label(info_frame, text="Age:", font=("Segoe UI", 9, "bold"), bg=self.card_color, fg=self.text_primary)
        self.lbl_age_val = tk.Label(info_frame, text="-", font=("Segoe UI", 9), bg=self.card_color, fg=self.text_secondary, anchor="w")
        
        self.lbl_gender_title = tk.Label(info_frame, text="Gender:", font=("Segoe UI", 9, "bold"), bg=self.card_color, fg=self.text_primary)
        self.lbl_gender_val = tk.Label(info_frame, text="-", font=("Segoe UI", 9), bg=self.card_color, fg=self.text_secondary, anchor="w")
        
        self.lbl_date_title = tk.Label(info_frame, text="Date of Adm:", font=("Segoe UI", 9, "bold"), bg=self.card_color, fg=self.text_primary)
        self.lbl_date_val = tk.Label(info_frame, text="-", font=("Segoe UI", 9), bg=self.card_color, fg=self.text_secondary, anchor="w")



        # Grid layouts
        self.lbl_admission_title.grid(row=0, column=0, sticky="w", pady=6)
        self.lbl_admission_val.grid(row=0, column=1, sticky="ew", pady=6)
        
        self.lbl_name_title.grid(row=0, column=2, sticky="w", pady=6)
        self.lbl_name_val.grid(row=0, column=3, sticky="ew", pady=6)
        
        self.lbl_age_title.grid(row=1, column=0, sticky="w", pady=6)
        self.lbl_age_val.grid(row=1, column=1, sticky="ew", pady=6)
        
        self.lbl_gender_title.grid(row=1, column=2, sticky="w", pady=6)
        self.lbl_gender_val.grid(row=1, column=3, sticky="ew", pady=6)
        
        self.lbl_date_title.grid(row=2, column=0, sticky="w", pady=6)
        self.lbl_date_val.grid(row=2, column=1, columnspan=3, sticky="ew", pady=6)



        # Setup standard Styles for tables
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Profile.Treeview",
            background=self.card_color,
            fieldbackground=self.card_color,
            foreground=self.text_primary,
            rowheight=26,
            bordercolor=self.entry_border,
            borderwidth=0,
            font=("Segoe UI", 9)
        )
        style.configure(
            "Profile.Treeview.Heading",
            background="#F1F5F9",
            foreground=self.primary_color,
            font=("Segoe UI", 9, "bold"),
            borderwidth=1,
            bordercolor=self.entry_border
        )
        style.map("Profile.Treeview", background=[('selected', self.secondary_color)], foreground=[('selected', "#FFFFFF")])

        # --- SECTION 2: Assigned Subjects List ---
        subjects_frame = tk.LabelFrame(
            self, text="Assigned Subjects", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.secondary_color, labelanchor="n", padx=15, pady=10,
            highlightbackground=self.entry_border, highlightthickness=1, bd=0
        )
        subjects_frame.pack(fill="x", padx=25, pady=5)

        # Treeview setup for Assigned Subjects
        sub_cols = ("Code", "Name")
        self.tree_subjects = ttk.Treeview(subjects_frame, columns=sub_cols, show="headings", height=4, style="Profile.Treeview")
        self.tree_subjects.heading("Code", text="Subject Code")
        self.tree_subjects.heading("Name", text="Subject Name")
        self.tree_subjects.column("Code", width=150, anchor="center")
        self.tree_subjects.column("Name", width=400, anchor="w")

        # Scrollbar for subjects
        sub_scroll = tk.Scrollbar(subjects_frame, orient="vertical", command=self.tree_subjects.yview)
        self.tree_subjects.configure(yscrollcommand=sub_scroll.set)

        self.tree_subjects.pack(side="left", fill="both", expand=True, pady=5)
        sub_scroll.pack(side="right", fill="y", pady=5)

        # --- SECTION 3: Results Table ---
        results_frame = tk.LabelFrame(
            self, text="Academic Results", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.success_color, labelanchor="n", padx=15, pady=10,
            highlightbackground=self.entry_border, highlightthickness=1, bd=0
        )
        results_frame.pack(fill="both", expand=True, padx=25, pady=(5, 15))

        # Treeview setup for Academic Results
        res_cols = ("Subject", "Assessment", "Exam", "Total")
        self.tree_results = ttk.Treeview(results_frame, columns=res_cols, show="headings", style="Profile.Treeview")
        self.tree_results.heading("Subject", text="Subject")
        self.tree_results.heading("Assessment", text="Assessment (30)")
        self.tree_results.heading("Exam", text="Exam (70)")
        self.tree_results.heading("Total", text="Total (100)")

        self.tree_results.column("Subject", width=250, anchor="w")
        self.tree_results.column("Assessment", width=110, anchor="center")
        self.tree_results.column("Exam", width=110, anchor="center")
        self.tree_results.column("Total", width=110, anchor="center")

        # Scrollbar for results
        res_scroll = tk.Scrollbar(results_frame, orient="vertical", command=self.tree_results.yview)
        self.tree_results.configure(yscrollcommand=res_scroll.set)

        self.tree_results.pack(side="left", fill="both", expand=True, pady=5)
        res_scroll.pack(side="right", fill="y", pady=5)

        # --- SECTION 4: Close Button ---
        self.btn_close = tk.Button(
            self, text="Close Profile", font=("Segoe UI", 11, "bold"),
            bg=self.accent_color, fg="#FFFFFF", relief="flat", bd=0,
            activebackground="#F87171", activeforeground="#FFFFFF",
            cursor="hand2", command=self.destroy
        )
        self.btn_close.pack(pady=(0, 20), ipady=8, ipadx=20)
        self.btn_close.bind("<Enter>", lambda e: self.btn_close.config(bg="#F87171"))
        self.btn_close.bind("<Leave>", lambda e: self.btn_close.config(bg=self.accent_color))

    def load_data(self):
        try:
            # 1. Load Student Personal Information
            profile = self.search_service.get_student_profile(self.student_id)
            if profile is None:
                messagebox.showerror("Error", "Student profile not found.")
                self.destroy()
                return

            self.lbl_admission_val.config(text=str(profile.admission_no))
            self.lbl_name_val.config(text=profile.full_name)
            self.lbl_age_val.config(text=str(profile.age))
            self.lbl_gender_val.config(text=profile.gender)
            self.lbl_date_val.config(text=str(profile.date_of_admission))



            # 2. Load Assigned Subjects
            subjects = self.search_service.get_student_subjects(self.student_id)
            for sub in subjects:
                self.tree_subjects.insert(
                    "",
                    tk.END,
                    values=(sub["subject_code"], sub["subject_name"])
                )

            # 3. Load Results
            results = self.search_service.get_student_results(self.student_id)
            for res in results:
                self.tree_results.insert(
                    "",
                    tk.END,
                    values=(
                        f"{res['subject_name']} ({res['subject_code']})",
                        f"{res['assessment_mark']:.1f}",
                        f"{res['exam_mark']:.1f}",
                        f"{res['total_mark']:.1f}"
                    )
                )

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load profile data: {e}")
            self.destroy()
