import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ui.student_profile_view import StudentProfileView
from utils.validators import StudentValidationError

class SearchView(tk.Frame):
    """
    Tkinter Student Search Screen.
    Inherits from tk.Frame to load inside the main window's content frame.
    Allows searching students by Admission Number or Name (with partial matching support).
    Displays results in a table and permits viewing the selected student's full profile.
    """

    def __init__(self, parent, search_service):
        super().__init__(parent, bg="#F8FAFC")
        self.search_service = search_service
        self.selected_student_id = None

        # Color palette (Professional Education theme)
        self.bg_color = "#F8FAFC"
        self.card_color = "#FFFFFF"
        self.text_color = "#111827"
        self.text_secondary = "#6B7280"
        self.primary_color = "#1E3A8A"   # Deep Blue
        self.secondary_color = "#3B82F6" # Bright Blue (Hover / Select Highlight)
        self.delete_color = "#EF4444"    # Red (Clear Button)
        self.entry_bg = "#F8FAFC"
        self.entry_fg = "#111827"
        self.entry_border = "#E2E8F0"

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Header Title
        header_frame = tk.Frame(self, bg=self.bg_color)
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text="Student Search Module",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
            anchor="w"
        )
        title_label.pack(fill="x")

        lbl_subtitle = tk.Label(
            header_frame,
            text="Search the student directory by Name or Admission Number. Double-click a row to open their profile.",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.text_secondary,
            anchor="w"
        )
        lbl_subtitle.pack(fill="x", pady=(2, 0))

        # --- UPPER CARD: Search Controls ---
        search_frame = tk.Frame(
            self,
            bg=self.card_color,
            padx=20,
            pady=15,
            highlightbackground=self.entry_border,
            highlightthickness=1,
            bd=0
        )
        search_frame.pack(fill="x", padx=30, pady=5)
        search_frame.columnconfigure(0, weight=1)
        search_frame.columnconfigure(1, weight=2)
        search_frame.columnconfigure(2, weight=1)

        # 1. Search Type Label & Combobox
        tk.Label(
            search_frame, text="Search By *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_color
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 2))

        # Style Combobox
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

        self.combo_type = ttk.Combobox(
            search_frame, font=("Segoe UI", 10), state="readonly", style="TCombobox"
        )
        self.combo_type['values'] = ("Admission Number", "Student Name")
        self.combo_type.current(0)
        self.combo_type.grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=3)

        # 2. Search Input Label & Entry
        tk.Label(
            search_frame, text="Search Term *", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_color
        ).grid(row=0, column=1, sticky="w", pady=(0, 2))

        self.entry_search = tk.Entry(
            search_frame, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.entry_fg,
            bd=0, highlightthickness=1, highlightbackground=self.entry_border,
            highlightcolor=self.primary_color, insertbackground=self.text_color
        )
        self.entry_search.grid(row=1, column=1, sticky="ew", ipady=5)
        self.entry_search.bind("<Return>", lambda e: self.perform_search())

        # 3. Search Button
        self.btn_search = tk.Button(
            search_frame, text="Search", font=("Segoe UI", 10, "bold"),
            bg=self.primary_color, fg="#FFFFFF", relief="flat", bd=0,
            cursor="hand2", activebackground=self.secondary_color, activeforeground="#FFFFFF",
            command=self.perform_search
        )
        self.btn_search.grid(row=1, column=2, sticky="ew", padx=(15, 0), ipady=8)
        self.btn_search.bind("<Enter>", lambda e: self.btn_search.config(bg=self.secondary_color))
        self.btn_search.bind("<Leave>", lambda e: self.btn_search.config(bg=self.primary_color))

        # --- LOWER CARD: Results Table ---
        table_frame = tk.LabelFrame(
            self, text="Search Results", font=("Segoe UI", 10, "bold"),
            bg=self.card_color, fg=self.primary_color, labelanchor="n", padx=10, pady=10,
            highlightbackground=self.entry_border, highlightthickness=1, bd=0
        )
        table_frame.pack(fill="both", expand=True, padx=30, pady=(15, 10))

        # Treeview setup
        style.configure(
            "Search.Treeview",
            background=self.card_color,
            fieldbackground=self.card_color,
            foreground=self.text_color,
            rowheight=28,
            bordercolor=self.entry_border,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Search.Treeview.Heading",
            background="#F1F5F9",
            foreground=self.primary_color,
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            bordercolor=self.entry_border
        )
        style.map("Search.Treeview", background=[('selected', self.secondary_color)], foreground=[('selected', "#FFFFFF")])

        cols = ("ID", "Admission No", "Full Name", "Age", "Gender")
        self.tree_results = ttk.Treeview(table_frame, columns=cols, show="headings", style="Search.Treeview")
        
        self.tree_results.heading("ID", text="ID")
        self.tree_results.heading("Admission No", text="Admission No")
        self.tree_results.heading("Full Name", text="Full Name")
        self.tree_results.heading("Age", text="Age")
        self.tree_results.heading("Gender", text="Gender")
        
        self.tree_results.column("ID", width=60, anchor="center")
        self.tree_results.column("Admission No", width=120, anchor="center")
        self.tree_results.column("Full Name", width=260, anchor="w")
        self.tree_results.column("Age", width=80, anchor="center")
        self.tree_results.column("Gender", width=100, anchor="center")

        # Scrollbar
        scroll = tk.Scrollbar(table_frame, orient="vertical", command=self.tree_results.yview)
        self.tree_results.configure(yscrollcommand=scroll.set)
        
        self.tree_results.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scroll.pack(side="right", fill="y", pady=5)

        # Double click a row to view profile directly
        self.tree_results.bind("<Double-1>", lambda e: self.open_profile_view())

        # --- LOWER ACTION BUTTONS ---
        action_frame = tk.Frame(self, bg=self.bg_color)
        action_frame.pack(fill="x", padx=30, pady=(5, 15))

        # View Profile Button
        self.btn_profile = tk.Button(
            action_frame, text="View Profile", font=("Segoe UI", 10, "bold"),
            bg=self.primary_color, fg="#FFFFFF", relief="flat", bd=0,
            cursor="hand2", activebackground=self.secondary_color, activeforeground="#FFFFFF",
            command=self.open_profile_view
        )
        self.btn_profile.pack(side="right", padx=(5, 0), ipady=8, ipadx=15)
        self.btn_profile.bind("<Enter>", lambda e: self.btn_profile.config(bg=self.secondary_color))
        self.btn_profile.bind("<Leave>", lambda e: self.btn_profile.config(bg=self.primary_color))

        # Clear Search & Results Button
        self.btn_clear = tk.Button(
            action_frame, text="Clear Search", font=("Segoe UI", 10, "bold"),
            bg=self.delete_color, fg="#FFFFFF", relief="flat", bd=0,
            cursor="hand2", activebackground="#F87171", activeforeground="#FFFFFF",
            command=self.clear_all
        )
        self.btn_clear.pack(side="right", padx=(0, 5), ipady=8, ipadx=15)
        self.btn_clear.bind("<Enter>", lambda e: self.btn_clear.config(bg="#F87171"))
        self.btn_clear.bind("<Leave>", lambda e: self.btn_clear.config(bg=self.delete_color))

    def perform_search(self):
        search_type = self.combo_type.get()
        search_term = self.entry_search.get().strip()

        # Validation: Search field is required
        if not search_term:
            messagebox.showwarning("Validation Warning", "Please enter a search term.")
            return

        self.clear_table()

        try:
            if search_type == "Admission Number":
                results = self.search_service.search_by_admission_no(search_term)
            else:
                results = self.search_service.search_by_name(search_term)

            # Handle no results found
            if not results:
                messagebox.showinfo("Search Result", "No matching students found.")
                return

            # Display matching students
            for s in results:
                self.tree_results.insert(
                    "",
                    tk.END,
                    iid=s.student_id,
                    values=(
                        s.student_id,
                        s.admission_no,
                        s.full_name,
                        s.age,
                        s.gender
                    )
                )

        except StudentValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Search query failed: {e}")

    def open_profile_view(self):
        selected_item = self.tree_results.selection()
        if not selected_item:
            messagebox.showwarning("Selection Warning", "Please select a student from the results table first.")
            return

        student_id = int(selected_item[0])
        # Open profile window
        StudentProfileView(self, student_id, self.search_service)

    def clear_all(self):
        self.entry_search.delete(0, tk.END)
        self.combo_type.current(0)
        self.clear_table()

    def clear_table(self):
        for item in self.tree_results.get_children():
            self.tree_results.delete(item)
