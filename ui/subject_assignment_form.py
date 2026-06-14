import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.validators import StudentValidationError

class SubjectAssignmentForm(tk.Toplevel):
    """
    Tkinter Subject Assignment Form.
    Allows assigning and removing subjects for students.
    """

    def __init__(self, parent, student_service, assignment_service):
        super().__init__(parent)
        self.student_service = student_service
        self.assignment_service = assignment_service
        self.selected_student_id = None
        
        # Window configuration (wide layout for side-by-side lists)
        self.title("Subject Assignment")
        self.geometry("680x480")
        self.resizable(False, False)
        
        # Theme colors
        self.bg_color = "#1e1e2e"
        self.card_color = "#252538"
        self.text_color = "#f8f8f2"
        self.primary_color = "#74c7ec"  # Blue for Title
        self.student_color = "#a6e3a1"  # Green
        self.subject_color = "#cba6f7"  # Purple
        self.delete_color = "#f38ba8"   # Red for Remove button
        self.entry_bg = "#313244"
        self.entry_fg = "#cdd6f4"
        
        self.configure(bg=self.bg_color)
        
        # Create UI components
        self.create_widgets()
        
        # Load students into dropdown
        self.populate_students()

    def create_widgets(self):
        # Header title
        title_label = tk.Label(
            self,
            text="Subject Assignment Module",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=15)
        
        # 1. Student Selection Area
        select_frame = tk.Frame(self, bg=self.card_color, padx=15, pady=15)
        select_frame.pack(fill="x", padx=25, pady=5)
        
        tk.Label(
            select_frame, text="Select Student *", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.text_color
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Combobox setup
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
            select_frame, font=("Segoe UI", 10), state="readonly", style="TCombobox"
        )
        self.combo_student.grid(row=0, column=1, sticky="ew")
        select_frame.columnconfigure(1, weight=1)
        
        # Bind combobox selection change
        self.combo_student.bind("<<ComboboxSelected>>", self.on_student_select)
        
        # 2. Side-by-Side Lists Area
        lists_frame = tk.Frame(self, bg=self.bg_color)
        lists_frame.pack(fill="both", expand=True, padx=25, pady=(15, 20))
        lists_frame.rowconfigure(0, weight=1)
        lists_frame.columnconfigure(0, weight=4) # Available list
        lists_frame.columnconfigure(1, weight=1) # Buttons center
        lists_frame.columnconfigure(2, weight=4) # Assigned list
        
        # --- LEFT: Available Subjects Frame ---
        left_frame = tk.LabelFrame(
            lists_frame, text="Available Subjects", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.student_color, labelanchor="n", padx=10, pady=10
        )
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        scroll_avail = tk.Scrollbar(left_frame)
        scroll_avail.pack(side="right", fill="y")
        
        self.list_available = tk.Listbox(
            left_frame, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.entry_fg,
            selectbackground=self.primary_color, selectforeground=self.bg_color,
            bd=0, highlightthickness=0, yscrollcommand=scroll_avail.set
        )
        self.list_available.pack(fill="both", expand=True)
        scroll_avail.config(command=self.list_available.yview)
        
        # --- CENTER: Action Buttons Frame ---
        center_frame = tk.Frame(lists_frame, bg=self.bg_color)
        center_frame.grid(row=0, column=1, sticky="center")
        
        # Assign Button (Available -> Assigned)
        self.btn_assign = tk.Button(
            center_frame, text="Assign ->", font=("Segoe UI", 10, "bold"),
            bg=self.student_color, fg=self.bg_color, relief="flat", bd=0,
            cursor="hand2", command=self.assign_subject
        )
        self.btn_assign.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Remove Button (Assigned -> Available)
        self.btn_remove = tk.Button(
            center_frame, text="<- Remove", font=("Segoe UI", 10, "bold"),
            bg=self.delete_color, fg=self.bg_color, relief="flat", bd=0,
            cursor="hand2", command=self.remove_subject
        )
        self.btn_remove.pack(fill="x", ipady=8)
        
        # --- RIGHT: Assigned Subjects Frame ---
        right_frame = tk.LabelFrame(
            lists_frame, text="Assigned Subjects", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.subject_color, labelanchor="n", padx=10, pady=10
        )
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        scroll_assign = tk.Scrollbar(right_frame)
        scroll_assign.pack(side="right", fill="y")
        
        self.list_assigned = tk.Listbox(
            right_frame, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.entry_fg,
            selectbackground=self.primary_color, selectforeground=self.bg_color,
            bd=0, highlightthickness=0, yscrollcommand=scroll_assign.set
        )
        self.list_assigned.pack(fill="both", expand=True)
        scroll_assign.config(command=self.list_assigned.yview)

    def populate_students(self):
        try:
            # Clear combobox
            self.combo_student['values'] = ()
            
            # Fetch all students from service
            students = self.student_service.get_all_students()
            
            options = ["Select Student"]
            for s in students:
                # Format: "Name (ID: student_id)"
                options.append(f"{s.full_name} (ID: {s.student_id})")
                
            self.combo_student['values'] = options
            self.combo_student.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {e}")

    def on_student_select(self, event):
        selected_text = self.combo_student.get()
        
        if selected_text == "Select Student":
            self.selected_student_id = None
            self.clear_lists()
            return
            
        try:
            # Parse student ID out of string: "Alice Vance (ID: 1)" -> 1
            parts = selected_text.split("(ID: ")
            self.selected_student_id = int(parts[1][:-1])
            
            # Refresh subject lists for this student
            self.refresh_lists()
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting student: {e}")

    def refresh_lists(self):
        if self.selected_student_id is None:
            self.clear_lists()
            return
            
        try:
            # 1. Fetch available and assigned lists from service
            available = self.assignment_service.get_available_subjects(self.selected_student_id)
            assigned = self.assignment_service.get_assigned_subjects(self.selected_student_id)
            
            # 2. Clear current listboxes
            self.list_available.delete(0, tk.END)
            self.list_assigned.delete(0, tk.END)
            
            # 3. Populate Available listbox (e.g. "Maths [ID: 1]")
            for sub in available:
                self.list_available.insert(tk.END, f"{sub.subject_name} ({sub.subject_code}) [ID: {sub.subject_id}]")
                
            # 4. Populate Assigned listbox
            for sub in assigned:
                self.list_assigned.insert(tk.END, f"{sub.subject_name} ({sub.subject_code}) [ID: {sub.subject_id}]")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh subject lists: {e}")

    def clear_lists(self):
        self.list_available.delete(0, tk.END)
        self.list_assigned.delete(0, tk.END)

    def assign_subject(self):
        # Verify a student is selected
        if self.selected_student_id is None:
            messagebox.showwarning("Warning", "Please select a student first.")
            return
            
        # Get selected item index from available listbox
        selection = self.list_available.curselection()
        if len(selection) == 0:
            messagebox.showwarning("Warning", "Please select a subject to assign from the left list.")
            return
            
        index = selection[0]
        item_text = self.list_available.get(index)
        
        try:
            # Parse subject ID out of string: "Mathematics (MAT-665) [ID: 1]" -> 1
            parts = item_text.split("[ID: ")
            subject_id = int(parts[1][:-1])
            
            # Save mapping using AssignmentService
            self.assignment_service.assign_subject_to_student(self.selected_student_id, subject_id)
            messagebox.showinfo("Success", "Subject assigned successfully!")
            
            # Refresh lists
            self.refresh_lists()
        except StudentValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to assign subject: {e}")

    def remove_subject(self):
        # Verify a student is selected
        if self.selected_student_id is None:
            messagebox.showwarning("Warning", "Please select a student first.")
            return
            
        # Get selected item index from assigned listbox
        selection = self.list_assigned.curselection()
        if len(selection) == 0:
            messagebox.showwarning("Warning", "Please select a subject to remove from the right list.")
            return
            
        index = selection[0]
        item_text = self.list_assigned.get(index)
        
        try:
            # Parse subject ID out of string
            parts = item_text.split("[ID: ")
            subject_id = int(parts[1][:-1])
            
            # Delete mapping using AssignmentService
            self.assignment_service.remove_subject_from_student(self.selected_student_id, subject_id)
            messagebox.showinfo("Success", "Subject removed successfully!")
            
            # Refresh lists
            self.refresh_lists()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to remove subject: {e}")
