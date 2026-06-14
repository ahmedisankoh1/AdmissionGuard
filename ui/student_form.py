import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from utils.validators import StudentValidationError

class StudentForm(tk.Toplevel):
    """
    Tkinter Student Registration Form.
    Inherits from tk.Toplevel so it can be opened from the main navigation hub.
    """

    def __init__(self, parent, student_service):
        # Initialize Toplevel window with parent
        super().__init__(parent)
        self.student_service = student_service
        
        # Window settings
        self.title("Student Management System - Registration")
        self.geometry("480x580")
        self.resizable(False, False)
        
        # Theme colors (Sleek dark mode)
        self.bg_color = "#1e1e2e"       # Dark background
        self.card_color = "#252538"     # Inside container background
        self.text_color = "#f8f8f2"     # Light white text
        self.primary_color = "#74c7ec"  # Light blue for Save Button
        self.accent_color = "#f38ba8"   # Pinkish red for Clear Button
        self.entry_bg = "#313244"       # Input box background
        self.entry_fg = "#cdd6f4"       # Input box text
        
        self.configure(bg=self.bg_color)
        
        # Draw the widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Header title
        title_label = tk.Label(
            self,
            text="Student Registration",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=15)
        
        # Card container to hold the forms
        self.form_frame = tk.Frame(
            self,
            bg=self.card_color,
            padx=25,
            pady=20
        )
        self.form_frame.pack(fill="x", padx=25, pady=5)
        
        # 1. Admission Number
        self.label_admission = tk.Label(
            self.form_frame, text="Admission Number *", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.text_color
        )
        self.label_admission.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.entry_admission = tk.Entry(
            self.form_frame, font=("Segoe UI", 11),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_color,
            bd=0, highlightthickness=1, highlightbackground="#45475a", highlightcolor=self.primary_color
        )
        self.entry_admission.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12), ipady=4)
        
        # 2. Full Name
        self.label_name = tk.Label(
            self.form_frame, text="Full Name *", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.text_color
        )
        self.label_name.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.entry_name = tk.Entry(
            self.form_frame, font=("Segoe UI", 11),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_color,
            bd=0, highlightthickness=1, highlightbackground="#45475a", highlightcolor=self.primary_color
        )
        self.entry_name.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12), ipady=4)
        
        # 3. Age
        self.label_age = tk.Label(
            self.form_frame, text="Age (14 - 20) *", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.text_color
        )
        self.label_age.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.entry_age = tk.Entry(
            self.form_frame, font=("Segoe UI", 11),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_color,
            bd=0, highlightthickness=1, highlightbackground="#45475a", highlightcolor=self.primary_color
        )
        self.entry_age.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 12), ipady=4)
        
        # 4. Gender (Dropdown)
        self.label_gender = tk.Label(
            self.form_frame, text="Gender *", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.text_color
        )
        self.label_gender.grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        # Configure modern style for Combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TCombobox",
            fieldbackground=self.entry_bg,
            background=self.entry_bg,
            foreground=self.entry_fg,
            arrowcolor=self.text_color
        )
        
        self.combo_gender = ttk.Combobox(
            self.form_frame, font=("Segoe UI", 11), state="readonly", style="TCombobox"
        )
        self.combo_gender['values'] = ("Select Gender", "Male", "Female", "Other")
        self.combo_gender.current(0)
        self.combo_gender.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 12), ipady=2)
        
        # 5. Date of Admission
        self.label_date = tk.Label(
            self.form_frame, text="Date of Admission (YYYY-MM-DD) *", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.text_color
        )
        self.label_date.grid(row=8, column=0, sticky="w", pady=(0, 5))
        
        self.entry_date = tk.Entry(
            self.form_frame, font=("Segoe UI", 11),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_color,
            bd=0, highlightthickness=1, highlightbackground="#45475a", highlightcolor=self.primary_color
        )
        # Prefill date box with today's date
        today_date = datetime.now().strftime("%Y-%m-%d")
        self.entry_date.insert(0, today_date)
        self.entry_date.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 10), ipady=4)
        
        # Make grid elements expand to fill space
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=1)
        
        # Button container frame
        btn_frame = tk.Frame(self, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=15, padx=25)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        # Clear Form Button
        self.btn_clear = tk.Button(
            btn_frame, text="Clear Form", font=("Segoe UI", 11, "bold"),
            bg=self.accent_color, fg=self.bg_color, relief="flat", bd=0,
            activebackground="#e07a5f", activeforeground=self.bg_color,
            cursor="hand2", command=self.clear_form
        )
        self.btn_clear.grid(row=0, column=0, padx=(0, 10), sticky="ew", ipady=8)
        
        # Save Student Button
        self.btn_save = tk.Button(
            btn_frame, text="Save Student", font=("Segoe UI", 11, "bold"),
            bg=self.primary_color, fg=self.bg_color, relief="flat", bd=0,
            activebackground="#a6e3a1", activeforeground=self.bg_color,
            cursor="hand2", command=self.save_student
        )
        self.btn_save.grid(row=0, column=1, padx=(10, 0), sticky="ew", ipady=8)

    def save_student(self):
        # Retrieve values from text entries
        admission_no = self.entry_admission.get()
        full_name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.combo_gender.get()
        date_of_admission = self.entry_date.get()
        
        try:
            # Call student_service to save student
            student = self.student_service.create_student(
                admission_no=admission_no,
                full_name=full_name,
                age=age,
                gender=gender,
                date_of_admission=date_of_admission
            )
            
            # Show success alert popup
            messagebox.showinfo(
                "Success", 
                f"Student '{student.full_name}' registered successfully!\nAssigned ID: {student.student_id}"
            )
            
            # Clear form boxes after success
            self.clear_form()
            
        except StudentValidationError as e:
            # Handle validation rule failures
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            # Handle unexpected database issues
            messagebox.showerror("Database Error", f"Failed to save student: {e}")

    def clear_form(self):
        # Wipe text entries clean
        self.entry_admission.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        
        # Reset gender combo to top selection
        self.combo_gender.current(0)
        
        # Reset date entry to current date
        self.entry_date.delete(0, tk.END)
        today_date = datetime.now().strftime("%Y-%m-%d")
        self.entry_date.insert(0, today_date)
