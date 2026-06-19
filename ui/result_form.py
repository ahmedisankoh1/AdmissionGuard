import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.validators import StudentValidationError

class ResultForm(tk.Toplevel):
    """
    Tkinter Result Management Form.
    Allows recording, updating, and viewing student results.
    """

    def __init__(self, parent, student_service, assignment_service, result_service):
        super().__init__(parent)
        self.student_service = student_service
        self.assignment_service = assignment_service
        self.result_service = result_service
        
        self.selected_student_id = None
        self.selected_result_id = None
        self.assigned_subjects = []  # List of Subject models for selected student

        # Window configuration
        self.title("Result Management")
        self.geometry("750x550")
        self.resizable(False, False)
        
        # Theme colors matching existing styles
        self.bg_color = "#1e1e2e"
        self.card_color = "#252538"
        self.text_color = "#f8f8f2"
        self.primary_color = "#74c7ec"   # Light Blue (Title)
        self.student_color = "#a6e3a1"   # Green (Save button)
        self.subject_color = "#cba6f7"   # Purple (Treeview columns)
        self.assign_color = "#f9e2af"    # Yellow (Calculate button)
        self.delete_color = "#f38ba8"    # Red (Clear button)
        self.entry_bg = "#313244"
        self.entry_fg = "#cdd6f4"
        
        self.configure(bg=self.bg_color)
        
        # Create UI components
        self.create_widgets()
        
        # Load students dropdown
        self.populate_students()

    def create_widgets(self):
        # Header Title
        title_label = tk.Label(
            self,
            text="Result Management Module",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=(15, 10))

        # --- UPPER CARD: Form Controls ---
        form_frame = tk.Frame(self, bg=self.card_color, padx=15, pady=15)
        form_frame.pack(fill="x", padx=25, pady=5)
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

        # Left Column: Selection
        left_column = tk.Frame(form_frame, bg=self.card_color)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        tk.Label(
            left_column, text="Select Student *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_color
        ).pack(anchor="w", pady=(0, 2))
        
        # Style Comboboxes
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TCombobox",
            fieldbackground=self.entry_bg,
            background=self.entry_bg,
            foreground=self.entry_fg,
            arrowcolor=self.text_color
        )
        
        self.combo_student = ttk.Combobox(
            left_column, font=("Segoe UI", 10), state="readonly", style="TCombobox"
        )
        self.combo_student.pack(fill="x", pady=(0, 10))
        self.combo_student.bind("<<ComboboxSelected>>", self.on_student_select)

        tk.Label(
            left_column, text="Select Subject *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_color
        ).pack(anchor="w", pady=(0, 2))
        
        self.combo_subject = ttk.Combobox(
            left_column, font=("Segoe UI", 10), state="readonly", style="TCombobox"
        )
        self.combo_subject.pack(fill="x")

        # Right Column: Marks Input
        right_column = tk.Frame(form_frame, bg=self.card_color)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        marks_grid = tk.Frame(right_column, bg=self.card_color)
        marks_grid.pack(fill="both", expand=True)
        marks_grid.columnconfigure(1, weight=1)

        tk.Label(
            marks_grid, text="Assessment Mark (0-30) *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_color
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.entry_assessment = tk.Entry(
            marks_grid, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.entry_fg,
            bd=0, highlightthickness=1, highlightbackground="#45475a",
            highlightcolor=self.primary_color, insertbackground=self.text_color
        )
        self.entry_assessment.grid(row=0, column=1, sticky="ew", padx=(10, 0), ipady=3)

        tk.Label(
            marks_grid, text="Exam Mark (0-70) *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_color
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        self.entry_exam = tk.Entry(
            marks_grid, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.entry_fg,
            bd=0, highlightthickness=1, highlightbackground="#45475a",
            highlightcolor=self.primary_color, insertbackground=self.text_color
        )
        self.entry_exam.grid(row=1, column=1, sticky="ew", padx=(10, 0), ipady=3)

        tk.Label(
            marks_grid, text="Total Mark (0-100)", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_color
        ).grid(row=2, column=0, sticky="w", pady=5)
        
        self.entry_total = tk.Entry(
            marks_grid, font=("Segoe UI", 10, "bold"), bg=self.entry_bg, fg=self.entry_fg,
            bd=0, highlightthickness=1, highlightbackground="#45475a",
            state="readonly"  # Make total read-only
        )
        self.entry_total.grid(row=2, column=1, sticky="ew", padx=(10, 0), ipady=3)

        # Action Buttons Container
        buttons_frame = tk.Frame(form_frame, bg=self.card_color)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=(15, 0))

        # Calculate Button
        self.btn_calculate = tk.Button(
            buttons_frame, text="Calculate Total", font=("Segoe UI", 9, "bold"),
            bg=self.assign_color, fg=self.bg_color, relief="flat", bd=0,
            cursor="hand2", command=self.calculate_total_display
        )
        self.btn_calculate.pack(side="left", padx=5, ipady=6, ipadx=10)

        # Save Button
        self.btn_save = tk.Button(
            buttons_frame, text="Save Result", font=("Segoe UI", 9, "bold"),
            bg=self.student_color, fg=self.bg_color, relief="flat", bd=0,
            cursor="hand2", command=self.save_result
        )
        self.btn_save.pack(side="left", padx=5, ipady=6, ipadx=10)

        # Clear Button
        self.btn_clear = tk.Button(
            buttons_frame, text="Clear Form", font=("Segoe UI", 9, "bold"),
            bg=self.delete_color, fg=self.bg_color, relief="flat", bd=0,
            cursor="hand2", command=self.clear_form
        )
        self.btn_clear.pack(side="left", padx=5, ipady=6, ipadx=10)

        # --- LOWER CARD: Results Table ---
        table_frame = tk.LabelFrame(
            self, text="Student Results Table", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.subject_color, labelanchor="n", padx=10, pady=10
        )
        table_frame.pack(fill="both", expand=True, padx=25, pady=(15, 20))

        # Customize Treeview style
        style.configure(
            "Treeview",
            background=self.entry_bg,
            fieldbackground=self.entry_bg,
            foreground=self.entry_fg,
            rowheight=24,
            font=("Segoe UI", 9)
        )
        style.configure(
            "Treeview.Heading",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Segoe UI", 9, "bold")
        )
        style.map("Treeview", background=[('selected', self.primary_color)], foreground=[('selected', self.bg_color)])

        # Treeview setup
        cols = ("Subject", "Assessment Mark", "Exam Mark", "Total Mark")
        self.tree_results = ttk.Treeview(table_frame, columns=cols, show="headings", style="Treeview")
        
        self.tree_results.heading("Subject", text="Subject")
        self.tree_results.heading("Assessment Mark", text="Assessment Mark (30)")
        self.tree_results.heading("Exam Mark", text="Exam Mark (70)")
        self.tree_results.heading("Total Mark", text="Total Mark (100)")
        
        self.tree_results.column("Subject", width=250, anchor="w")
        self.tree_results.column("Assessment Mark", width=130, anchor="center")
        self.tree_results.column("Exam Mark", width=130, anchor="center")
        self.tree_results.column("Total Mark", width=130, anchor="center")

        # Scrollbar
        scroll = tk.Scrollbar(table_frame, orient="vertical", command=self.tree_results.yview)
        self.tree_results.configure(yscrollcommand=scroll.set)
        
        self.tree_results.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Double click to select/edit result
        self.tree_results.bind("<Double-1>", self.on_row_select)

    def populate_students(self):
        try:
            self.combo_student['values'] = ()
            students = self.student_service.get_all_students()
            options = ["Select Student"]
            for s in students:
                options.append(f"{s.full_name} (ID: {s.student_id})")
            self.combo_student['values'] = options
            self.combo_student.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {e}")

    def on_student_select(self, event):
        selected_text = self.combo_student.get()
        if selected_text == "Select Student":
            self.selected_student_id = None
            self.assigned_subjects = []
            self.combo_subject['values'] = ()
            self.combo_subject.set("")
            self.clear_table()
            return

        try:
            # Parse student ID: "Full Name (ID: 1)" -> 1
            parts = selected_text.split("(ID: ")
            self.selected_student_id = int(parts[1][:-1])

            # Load only assigned subjects for the selected student
            self.assigned_subjects = self.assignment_service.get_assigned_subjects(self.selected_student_id)
            
            subject_options = []
            for sub in self.assigned_subjects:
                subject_options.append(f"{sub.subject_name} (ID: {sub.subject_id})")

            self.combo_subject['values'] = subject_options
            if len(subject_options) > 0:
                self.combo_subject.current(0)
            else:
                self.combo_subject.set("")

            # Refresh table
            self.refresh_results_table()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading student details: {e}")

    def calculate_total_display(self):
        """
        Validates input bounds in UI layer and displays calculated sum.
        """
        am_text = self.entry_assessment.get().strip()
        em_text = self.entry_exam.get().strip()

        try:
            if am_text == "" or em_text == "":
                messagebox.showwarning("Warning", "Please enter values for both Assessment and Exam Marks.")
                return None
                
            total = self.result_service.calculate_total(am_text, em_text)
            
            # Update read-only field
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, f"{total:.1f}")
            self.entry_total.config(state="readonly")
            return total
        except StudentValidationError as e:
            messagebox.showerror("Validation Error", str(e))
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {e}")
            return None

    def save_result(self):
        if self.selected_student_id is None:
            messagebox.showwarning("Warning", "Please select a student first.")
            return

        # Fetch subject selection
        subject_text = self.combo_subject.get()
        if not subject_text:
            messagebox.showwarning("Warning", "Please select a subject.")
            return

        try:
            # Parse subject_id: "Mathematic (ID: 1)" -> 1
            parts = subject_text.split("(ID: ")
            subject_id = int(parts[1][:-1])
        except Exception:
            messagebox.showerror("Error", "Invalid subject selection format.")
            return

        am_text = self.entry_assessment.get().strip()
        em_text = self.entry_exam.get().strip()

        try:
            if self.selected_result_id is None:
                # Insert mode
                self.result_service.save_result(
                    student_id=self.selected_student_id,
                    subject_id=subject_id,
                    assessment_mark=am_text,
                    exam_mark=em_text
                )
                messagebox.showinfo("Success", "Result saved successfully!")
            else:
                # Edit mode
                self.result_service.update_result(
                    result_id=self.selected_result_id,
                    assessment_mark=am_text,
                    exam_mark=em_text
                )
                messagebox.showinfo("Success", "Result updated successfully!")
            
            self.clear_form(reset_student=False)
            self.refresh_results_table()
        except StudentValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save result: {e}")

    def refresh_results_table(self):
        self.clear_table()
        if self.selected_student_id is None:
            return

        try:
            results = self.result_service.get_student_results(self.selected_student_id)
            for r in results:
                self.tree_results.insert(
                    "",
                    tk.END,
                    iid=r["result_id"],
                    values=(
                        f"{r['subject_name']} ({r['subject_code']})",
                        r["assessment_mark"],
                        r["exam_mark"],
                        r["total_mark"]
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load results table: {e}")

    def on_row_select(self, event):
        """
        Triggers edit mode when double-clicking a row.
        Populates fields with row values and disables subject change.
        """
        selected_item = self.tree_results.selection()
        if not selected_item:
            return

        result_id = int(selected_item[0])
        values = self.tree_results.item(result_item:=selected_item[0], "values")
        
        # Set selection tracking
        self.selected_result_id = result_id

        # Find subject name and code to set combobox
        subject_str = values[0] # e.g. "English (ENG-461)"
        
        # Populate mark entries
        self.entry_assessment.delete(0, tk.END)
        self.entry_assessment.insert(0, str(values[1]))
        
        self.entry_exam.delete(0, tk.END)
        self.entry_exam.insert(0, str(values[2]))

        # Calculate display
        self.calculate_total_display()

        # Update subject Combobox text and disable it during edit mode
        # Match subject name inside assigned_subjects to find ID
        for sub in self.assigned_subjects:
            match_str = f"{sub.subject_name} ({sub.subject_code})"
            if match_str == subject_str:
                self.combo_subject.set(f"{sub.subject_name} (ID: {sub.subject_id})")
                break
        
        self.combo_subject.config(state="disabled")
        self.btn_save.config(text="Update Result", bg=self.primary_color)

    def clear_form(self, reset_student=True):
        self.selected_result_id = None
        
        self.entry_assessment.delete(0, tk.END)
        self.entry_exam.delete(0, tk.END)
        
        self.entry_total.config(state="normal")
        self.entry_total.delete(0, tk.END)
        self.entry_total.config(state="readonly")
        
        self.combo_subject.config(state="readonly")
        
        if reset_student:
            self.combo_student.current(0)
            self.selected_student_id = None
            self.combo_subject.set("")
            self.combo_subject['values'] = ()
            self.clear_table()
        else:
            # Keep student, but reset subject to default if possible
            if self.combo_subject['values']:
                self.combo_subject.current(0)
            else:
                self.combo_subject.set("")

        self.btn_save.config(text="Save Result", bg=self.student_color)

    def clear_table(self):
        for item in self.tree_results.get_children():
            self.tree_results.delete(item)
