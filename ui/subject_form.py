import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.validators import StudentValidationError

class SubjectForm(tk.Frame):
    """
    Tkinter Subject Management Form.
    Inherits from tk.Frame to load inside the main window's content frame.
    """

    def __init__(self, parent, subject_service):
        super().__init__(parent)
        self.subject_service = subject_service
        self.selected_subject_id = None
        
        # Color palette (Professional Education theme)
        self.bg_color = "#F8FAFC"
        self.card_color = "#FFFFFF"
        self.text_primary = "#111827"
        self.text_secondary = "#6B7280"
        self.primary_color = "#1E3A8A"   # Deep Blue
        self.secondary_color = "#3B82F6" # Bright Blue
        self.edit_color = "#F59E0B"      # Amber
        self.delete_color = "#EF4444"    # Red
        self.entry_bg = "#F8FAFC"
        self.entry_fg = "#111827"
        self.entry_border = "#E2E8F0"
        
        self.configure(bg=self.bg_color)
        
        # Setup modern Treeview styles
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
            foreground=self.text_primary,
            rowheight=28,
            bordercolor=self.entry_border,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        
        # Style the Treeview headers
        style.configure(
            "Custom.Treeview.Heading",
            background="#F1F5F9",
            foreground=self.primary_color,
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            bordercolor=self.entry_border
        )
        
        # Change color of selected row in table
        style.map(
            "Custom.Treeview",
            background=[('selected', self.secondary_color)],
            foreground=[('selected', "#FFFFFF")]
        )

    def create_widgets(self):
        # Header title
        header_frame = tk.Frame(self, bg=self.bg_color)
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text="Subject Management",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
            anchor="w"
        )
        title_label.pack(fill="x")

        lbl_subtitle = tk.Label(
            header_frame,
            text="Add, edit, or delete academic subjects in the database.",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.text_secondary,
            anchor="w"
        )
        lbl_subtitle.pack(fill="x", pady=(2, 0))
        
        # Form Container frame
        form_frame = tk.Frame(
            self,
            bg=self.card_color,
            padx=20,
            pady=20,
            highlightbackground=self.entry_border,
            highlightthickness=1,
            bd=0
        )
        form_frame.pack(fill="x", padx=30, pady=5)
        
        # Subject Name Label
        self.label_name = tk.Label(
            form_frame, text="Subject Name *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_primary
        )
        self.label_name.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Subject Name Input
        self.entry_name = tk.Entry(
            form_frame, font=("Segoe UI", 10),
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.text_primary,
            bd=0, highlightthickness=1, highlightbackground=self.entry_border, highlightcolor=self.primary_color
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
            bg=self.primary_color, fg="#FFFFFF", relief="flat", bd=0,
            cursor="hand2", activebackground=self.secondary_color, activeforeground="#FFFFFF",
            command=self.add_subject
        )
        self.btn_add.grid(row=0, column=0, padx=5, ipady=8, sticky="ew")
        self.btn_add.bind("<Enter>", lambda e: self.btn_add.config(bg=self.secondary_color))
        self.btn_add.bind("<Leave>", lambda e: self.btn_add.config(bg=self.primary_color))
        
        # Edit Button
        self.btn_edit = tk.Button(
            btn_bar, text="Edit Subject", font=("Segoe UI", 10, "bold"),
            bg=self.edit_color, fg="#FFFFFF", relief="flat", bd=0,
            cursor="hand2", activebackground="#FBBF24", activeforeground="#FFFFFF",
            command=self.edit_subject
        )
        self.btn_edit.grid(row=0, column=1, padx=5, ipady=8, sticky="ew")
        self.btn_edit.bind("<Enter>", lambda e: self.btn_edit.config(bg="#FBBF24"))
        self.btn_edit.bind("<Leave>", lambda e: self.btn_edit.config(bg=self.edit_color))
        
        # Delete Button
        self.btn_delete = tk.Button(
            btn_bar, text="Delete Subject", font=("Segoe UI", 10, "bold"),
            bg=self.delete_color, fg="#FFFFFF", relief="flat", bd=0,
            cursor="hand2", activebackground="#F87171", activeforeground="#FFFFFF",
            command=self.delete_subject
        )
        self.btn_delete.grid(row=0, column=2, padx=5, ipady=8, sticky="ew")
        self.btn_delete.bind("<Enter>", lambda e: self.btn_delete.config(bg="#F87171"))
        self.btn_delete.bind("<Leave>", lambda e: self.btn_delete.config(bg=self.delete_color))
        
        # List / Table Container Frame
        table_frame = tk.Frame(
            self,
            bg=self.card_color,
            highlightbackground=self.entry_border,
            highlightthickness=1,
            bd=0
        )
        table_frame.pack(fill="both", expand=True, padx=30, pady=(15, 20))
        
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
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
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
