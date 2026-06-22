import tkinter as tk
from tkinter import ttk

class DashboardView(tk.Frame):
    """
    Dashboard screen loaded inside the main window's content frame.
    Displays metrics cards and quick access options.
    """

    def __init__(self, parent, db_manager, nav_callback):
        super().__init__(parent, bg="#F8FAFC")
        self.db_manager = db_manager
        self.nav_callback = nav_callback

        # Palette colors
        self.bg_color = "#F8FAFC"
        self.card_bg = "#FFFFFF"
        self.primary_color = "#1E3A8A"
        self.secondary_color = "#3B82F6"
        self.text_primary = "#111827"
        self.text_secondary = "#6B7280"
        self.border_color = "#E2E8F0"

        # Build UI layout
        self.create_widgets()
        self.refresh_stats()

    def create_widgets(self):
        # 1. Header Frame
        header_frame = tk.Frame(self, bg=self.bg_color)
        header_frame.pack(fill="x", padx=30, pady=(25, 15))

        lbl_welcome = tk.Label(
            header_frame, text="Admission Guard Dashboard",
            font=("Segoe UI", 18, "bold"), bg=self.bg_color, fg=self.primary_color,
            anchor="w"
        )
        lbl_welcome.pack(fill="x")

        lbl_subtitle = tk.Label(
            header_frame, text="Overview of your student management system metrics and quick shortcuts.",
            font=("Segoe UI", 10), bg=self.bg_color, fg=self.text_secondary,
            anchor="w"
        )
        lbl_subtitle.pack(fill="x", pady=(2, 0))

        # 2. Stats Grid Container
        stats_frame = tk.Frame(self, bg=self.bg_color)
        stats_frame.pack(fill="x", padx=30, pady=10)
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)
        stats_frame.columnconfigure(3, weight=1)

        # Stat cards definitions
        self.cards = {}
        metrics = [
            ("Total Students", "students", self.secondary_color),
            ("Registered Subjects", "subjects", "#CBA6F7"), # Purple accent
            ("Active Assignments", "assignments", "#F9E2AF"), # Yellow accent
            ("Recorded Results", "results", "#10B981") # Green accent
        ]

        for idx, (label, key, color) in enumerate(metrics):
            card = tk.Frame(
                stats_frame, bg=self.card_bg, highlightbackground=self.border_color,
                highlightthickness=1, bd=0
            )
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")

            # Colored accent top border indicator
            accent_bar = tk.Frame(card, bg=color, height=4)
            accent_bar.pack(fill="x")

            # Labels and values
            lbl_card_title = tk.Label(
                card, text=label, font=("Segoe UI", 9, "bold"),
                bg=self.card_bg, fg=self.text_secondary, anchor="w", padx=15, pady=8
            )
            lbl_card_title.pack(fill="x")

            lbl_val = tk.Label(
                card, text="0", font=("Segoe UI", 24, "bold"),
                bg=self.card_bg, fg=self.text_primary, anchor="w", padx=15, pady=0
            )
            lbl_val.pack(fill="x", pady=(0, 15))
            self.cards[key] = lbl_val

        # 3. Quick Actions Card Frame
        actions_card = tk.Frame(
            self, bg=self.card_bg, highlightbackground=self.border_color,
            highlightthickness=1, bd=0, padx=25, pady=25
        )
        actions_card.pack(fill="both", expand=True, padx=40, pady=(15, 30))

        lbl_actions_title = tk.Label(
            actions_card, text="Quick Shortcuts", font=("Segoe UI", 12, "bold"),
            bg=self.card_bg, fg=self.primary_color, anchor="w"
        )
        lbl_actions_title.pack(fill="x", pady=(0, 15))

        btn_container = tk.Frame(actions_card, bg=self.card_bg)
        btn_container.pack(fill="x")
        btn_container.columnconfigure(0, weight=1)
        btn_container.columnconfigure(1, weight=1)
        btn_container.columnconfigure(2, weight=1)

        # Navigation shortcuts mapping
        shortcuts = [
            ("Manage Students", "Students", self.primary_color),
            ("Manage Subjects", "Subjects", self.primary_color),
            ("Subject Assignments", "Assignments", self.primary_color),
            ("Grade Results", "Results", self.primary_color),
            ("Search Directory", "Search", self.primary_color)
        ]

        # Grid the shortcuts
        for idx, (label, target, color) in enumerate(shortcuts):
            row = idx // 3
            col = idx % 3
            
            btn = tk.Button(
                btn_container, text=label, font=("Segoe UI", 10, "bold"),
                bg="#E2E8F0", fg=self.text_primary, relief="flat", bd=0,
                cursor="hand2", activebackground="#CBD5E1", activeforeground=self.text_primary,
                command=lambda t=target: self.nav_callback(t)
            )
            btn.grid(row=row, column=col, padx=10, pady=10, ipady=12, sticky="ew")

            # Bind hover animations
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#CBD5E1"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#E2E8F0"))

    def refresh_stats(self):
        """
        Queries counts from the database and updates card values dynamically.
        """
        try:
            # Query counts
            r_students = self.db_manager.fetch_one("SELECT COUNT(*) FROM students;")
            r_subjects = self.db_manager.fetch_one("SELECT COUNT(*) FROM subjects;")
            r_assignments = self.db_manager.fetch_one("SELECT COUNT(*) FROM student_subjects;")
            r_results = self.db_manager.fetch_one("SELECT COUNT(*) FROM results;")

            count_students = r_students[0] if r_students else 0
            count_subjects = r_subjects[0] if r_subjects else 0
            count_assignments = r_assignments[0] if r_assignments else 0
            count_results = r_results[0] if r_results else 0

            # Update labels
            self.cards["students"].config(text=str(count_students))
            self.cards["subjects"].config(text=str(count_subjects))
            self.cards["assignments"].config(text=str(count_assignments))
            self.cards["results"].config(text=str(count_results))
        except Exception as e:
            print(f"Error fetching dashboard statistics: {e}")
