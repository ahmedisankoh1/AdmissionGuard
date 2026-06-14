import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.validators import StudentValidationError

class SubjectForm(tk.Toplevel):
    """
    Tkinter Subject Management Form.
    Inherits from tk.Toplevel and allows adding, editing, and deleting subjects.
    """

    def __init__(self, parent, subject_service):
        super().__init__(parent)
        self.subject_service = subject_service
        self.selected_subject_id = None
        
        # Window configuration
        self.title("Subject Management")
        self.geometry("520x620")
        self.resizable(False, False)
        
        # Theme colors (Sleek dark mode matching StudentForm)
        self.bg_color = "#1e1e2e"
        self.card_color = "#252538"
        self.text_color = "#f8f8f2"
        self.primary_color = "#74c7ec"  # Blue for Add button
        self.edit_color = "#f9e2af"     # Yellow for Edit button
        self.delete_color = "#f38ba8"   # Red for Delete button
        self.entry_bg = "#313244"
        self.entry_fg = "#cdd6f4"
        
        self.configure(bg=self.bg_color)
        
        # Setup modern Treeview and combobox styles
        self.setup_styles()
        
        # Create UI components
        self.create_widgets()
        
        # Load subjects from database
        self.refresh_list()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style the Treeview container
        style.configure(
            "Custom.Treeview",
            background=self.card_color,
            fieldbackground=self.card_color,
            foreground=self.text_color,
            rowheight=28,
            bordercolor="#45475a",
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        
        # Style the Treeview headers
        style.configure(
            "Custom.Treeview.Heading",
            background=self.entry_bg,
            foreground=self.primary_color,
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            bordercolor="#45475a"
        )
        
        # Change color of selected row in table
        style.map(
            "Custom.Treeview",
            background=[('selected', self.primary_color)],
            foreground=[('selected', self.bg_color)]
        )

    def create_widgets(self):
        # Header title
        title_label = tk.Label(
            self,
            text="Subject Management",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=15)
        
        # Form Container frame
        form_frame = tk.Frame(self, bg=self.card_color, padx=20, pady=20)
        form_frame.pack(fill="x", padx=25, pady=5)
        
        # Subject Name Label
        self.label_name = tk.Label(
            form_frame, text="Subject Name *", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.text_color
        )
        self.label_name.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Subject Name Input
        self.entry_name = tk.Entry(
            form_frame, font=("Segoe UI", 11),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_color,
            bd=0, highlightthickness=1, highlightbackground="#45475a", highlightcolor=self.primary_color
        )
        self.entry_name.grid(row=1, column=0, sticky="ew", pady=(0, 15), ipady=5)
        form_frame.columnconfigure(0, weight=1)
        
        # Button bar inside container
        btn_bar = tk.Frame(form_frame, bg=self.card_color)
        btn_bar.grid(row=2, column=0, sticky="ew", pady=(5, 0))
        btn_bar.columnconfigure(0, weight=1)
        btn_bar.columnconfigure(1, weight=1)
        btn_bar.columnconfigure(2, weight=1)
        
        # Add Button
        self.btn_add = tk.Button(
            btn_bar, text="Add Subject", font=("Segoe UI", 10, "bold"),
            bg=self.primary_color, fg=self.bg_color, relief="flat", bd=0,
            cursor="hand2", command=self.add_subject
        )
        self.btn_add.grid(row=0, column=0, padx=5, ipady=6, sticky="ew")
        
        # Edit Button
        self.btn_edit = tk.Button(
            btn_bar, text="Edit Subject", font=("Segoe UI", 10, "bold"),
            bg=self.edit_color, fg=self.bg_color, relief="flat", bd=0,
            cursor="hand2", command=self.edit_subject
        )
        self.btn_edit.grid(row=0, column=1, padx=5, ipady=6, sticky="ew")
        
        # Delete Button
        self.btn_delete = tk.Button(
            btn_bar, text="Delete Subject", font=("Segoe UI", 10, "bold"),
            bg=self.delete_color, fg=self.bg_color, relief="flat", bd=0,
            cursor="hand2", command=self.delete_subject
        )
        self.btn_delete.grid(row=0, column=2, padx=5, ipady=6, sticky="ew")
        
        # List / Table Container Frame
        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill="both", expand=True, padx=25, pady=(15, 20))
        
        # Table Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview Table representing Subject ID and Name
        self.tree = ttk.Treeview(
            table_frame, columns=("ID", "Name"), show="headings",
            yscrollcommand=scrollbar.set, style="Custom.Treeview"
        )
        self.tree.heading("ID", text="Subject ID", anchor="w")
        self.tree.heading("Name", text="Subject Name", anchor="w")
        
        self.tree.column("ID", width=120, stretch=False)
        self.tree.column("Name", width=300, stretch=True)
        
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Bind double click or row select event
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def refresh_list(self):
        # Clear all existing table rows
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Fetch fresh list of subjects
            subjects = self.subject_service.get_all_subjects()
            for sub in subjects:
                # Insert row into tree
                self.tree.insert("", "end", values=(sub.subject_id, sub.subject_name))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subjects: {e}")

    def on_row_select(self, event):
        # Triggered when user selects a row in the treeview
        selected = self.tree.selection()
        if len(selected) > 0:
            item_id = selected[0]
            values = self.tree.item(item_id, "values")
            
            # Store selected subject ID and write name to entry box
            self.selected_subject_id = int(values[0])
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, values[1])
        else:
            self.selected_subject_id = None

    def add_subject(self):
        name = self.entry_name.get()
        try:
            # Save new subject
            sub = self.subject_service.create_subject(name)
            messagebox.showinfo("Success", f"Subject '{sub.subject_name}' added successfully!\nAssigned ID: {sub.subject_id}")
            
            # Reset UI selection
            self.clear_selection()
            self.refresh_list()
        except StudentValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save subject: {e}")

    def edit_subject(self):
        # Make sure user selected a subject to edit
        if self.selected_subject_id is None:
            messagebox.showwarning("Warning", "Please select a subject from the list to edit.")
            return
            
        new_name = self.entry_name.get()
        try:
            # Update subject name
            success = self.subject_service.update_subject(self.selected_subject_id, new_name)
            if success:
                messagebox.showinfo("Success", "Subject updated successfully!")
                self.clear_selection()
                self.refresh_list()
            else:
                messagebox.showerror("Error", "Failed to update subject (Subject ID not found).")
        except StudentValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update subject: {e}")

    def delete_subject(self):
        # Make sure user selected a subject to delete
        if self.selected_subject_id is None:
            messagebox.showwarning("Warning", "Please select a subject from the list to delete.")
            return
            
        subject_name = self.entry_name.get()
        
        # Open confirmation dialog before deleting
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete subject '{subject_name}'?\nThis will remove it from the system."
        )
        
        if confirm:
            try:
                # Delete subject
                success = self.subject_service.delete_subject(self.selected_subject_id)
                if success:
                    messagebox.showinfo("Success", f"Subject '{subject_name}' deleted successfully!")
                    self.clear_selection()
                    self.refresh_list()
                else:
                    messagebox.showerror("Error", "Failed to delete subject.")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to delete subject: {e}")

    def clear_selection(self):
        # Deselect current tree selection and clear text box
        self.tree.selection_remove(self.tree.selection())
        self.entry_name.delete(0, tk.END)
        self.selected_subject_id = None
