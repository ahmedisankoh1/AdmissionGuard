import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from utils.validators import StudentValidationError

class StudentForm(tk.Frame):
    """
    Tkinter Student Registration Form.
    Inherits from tk.Frame to load inside the main window's content frame.
    """

    def __init__(self, parent, student_service):
        super().__init__(parent)
        self.student_service = student_service
        
        # Color palette (Professional Education theme)
        self.bg_color = "#F8FAFC"
        self.card_color = "#FFFFFF"
        self.text_primary = "#111827"
        self.text_secondary = "#6B7280"
        self.primary_color = "#1E3A8A"   # Deep Blue
        self.secondary_color = "#3B82F6" # Bright Blue
        self.accent_color = "#EF4444"    # Red
        self.entry_bg = "#F8FAFC"
        self.entry_fg = "#111827"
        self.entry_border = "#E2E8F0"
        
        self.configure(bg=self.bg_color)
        
        # Draw the widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Header title frame
        header_frame = tk.Frame(self, bg=self.bg_color)
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text="Student Registration",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
            anchor="w"
        )
        title_label.pack(fill="x")
        
        lbl_subtitle = tk.Label(
            header_frame,
            text="Register a new student in the database. All fields marked with * are required.",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.text_secondary,
            anchor="w"
        )
        lbl_subtitle.pack(fill="x", pady=(2, 0))
        
        # Card container to hold the forms
        self.form_frame = tk.Frame(
            self,
            bg=self.card_color,
            padx=30,
            pady=25,
            highlightbackground=self.entry_border,
            highlightthickness=1,
            bd=0
        )
        self.form_frame.pack(fill="x", padx=30, pady=10)
        
        # Grid layout configurations for columns
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=1)
        
        # 1. Admission Number
        self.label_admission = tk.Label(
            self.form_frame, text="Admission Number *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_primary
        )
        self.label_admission.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        
        self.entry_admission = tk.Entry(
            self.form_frame, font=("Segoe UI", 10),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_primary,
            bd=0, highlightthickness=1, highlightbackground=self.entry_border, highlightcolor=self.primary_color
        )
        self.entry_admission.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=5)
        
        # 2. Full Name
        self.label_name = tk.Label(
            self.form_frame, text="Full Name *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_primary
        )
        self.label_name.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))
        
        self.entry_name = tk.Entry(
            self.form_frame, font=("Segoe UI", 10),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_primary,
            bd=0, highlightthickness=1, highlightbackground=self.entry_border, highlightcolor=self.primary_color
        )
        self.entry_name.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=5)
        
        # 3. Age
        self.label_age = tk.Label(
            self.form_frame, text="Age (14 - 20) *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_primary
        )
        self.label_age.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.entry_age = tk.Entry(
            self.form_frame, font=("Segoe UI", 10),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_primary,
            bd=0, highlightthickness=1, highlightbackground=self.entry_border, highlightcolor=self.primary_color
        )
        self.entry_age.grid(row=5, column=0, sticky="ew", pady=(0, 15), ipady=5, padx=(0, 10))
        
        # 4. Gender (Dropdown)
        self.label_gender = tk.Label(
            self.form_frame, text="Gender *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_primary
        )
        self.label_gender.grid(row=4, column=1, sticky="w", pady=(0, 5))
        
        # Configure style for Combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TCombobox",
            fieldbackground=self.entry_bg,
            background=self.entry_bg,
            foreground=self.entry_fg,
            arrowcolor=self.primary_color,
            bordercolor=self.entry_border
        )
        
        self.combo_gender = ttk.Combobox(
            self.form_frame, font=("Segoe UI", 10), state="readonly", style="TCombobox"
        )
        self.combo_gender['values'] = ("Select Gender", "Male", "Female", "Other")
        self.combo_gender.current(0)
        self.combo_gender.grid(row=5, column=1, sticky="ew", pady=(0, 15), ipady=4)
        
        # 5. Date of Admission
        self.label_date = tk.Label(
            self.form_frame, text="Date of Admission (YYYY-MM-DD) *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_primary
        )
        self.label_date.grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 5))
        
        self.entry_date = tk.Entry(
            self.form_frame, font=("Segoe UI", 10),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_primary,
            bd=0, highlightthickness=1, highlightbackground=self.entry_border, highlightcolor=self.primary_color
        )
        # Prefill date box with today's date
        today_date = datetime.now().strftime("%Y-%m-%d")
        self.entry_date.insert(0, today_date)
        self.entry_date.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 5), ipady=5)
        
        # Button container frame inside form_frame
        btn_frame = tk.Frame(self.form_frame, bg=self.card_color)
        btn_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        # Clear Form Button
        self.btn_clear = tk.Button(
            btn_frame, text="Clear Form", font=("Segoe UI", 10, "bold"),
            bg=self.accent_color, fg="#FFFFFF", relief="flat", bd=0,
            activebackground="#F87171", activeforeground="#FFFFFF",
            cursor="hand2", command=self.clear_form
        )
        self.btn_clear.grid(row=0, column=0, padx=(0, 10), sticky="ew", ipady=8)
        self.btn_clear.bind("<Enter>", lambda e: self.btn_clear.config(bg="#F87171"))
        self.btn_clear.bind("<Leave>", lambda e: self.btn_clear.config(bg=self.accent_color))
        
        # Save Student Button
        self.btn_save = tk.Button(
            btn_frame, text="Save Student", font=("Segoe UI", 10, "bold"),
            bg=self.primary_color, fg="#FFFFFF", relief="flat", bd=0,
            activebackground=self.secondary_color, activeforeground="#FFFFFF",
            cursor="hand2", command=self.save_student
        )
        self.btn_save.grid(row=0, column=1, padx=(10, 0), sticky="ew", ipady=8)
        self.btn_save.bind("<Enter>", lambda e: self.btn_save.config(bg=self.secondary_color))
        self.btn_save.bind("<Leave>", lambda e: self.btn_save.config(bg=self.primary_color))

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
            # Handle validation failures
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
