import tkinter as tk
from tkinter import messagebox
from utils.validators import StudentValidationError

class LoginForm(tk.Toplevel):
    """
    Tkinter Login Window.
    Allows user authentication and restricts system access.
    """

    def __init__(self, parent, auth_service, on_success):
        super().__init__(parent)
        self.auth_service = auth_service
        self.on_success = on_success

        self.title("Admission Guard - Login")
        self.geometry("380x450")
        self.resizable(False, False)

        # Audit color palette (Professional Education theme)
        self.bg_color = "#1E293B"       # Dark Slate background
        self.card_color = "#FFFFFF"     # White Card
        self.text_primary = "#111827"   # Charcoal Dark Text
        self.text_secondary = "#6B7280" # Gray secondary text
        self.primary_color = "#1E3A8A"   # Deep Blue Login Button
        self.hover_color = "#3B82F6"     # Bright Blue Hover
        self.entry_bg = "#F8FAFC"       # Very light slate/gray
        self.entry_border = "#E2E8F0"   # Light border
        
        self.configure(bg=self.bg_color)
        
        self.create_widgets()

    def create_widgets(self):
        # Top Spacer
        spacer = tk.Frame(self, bg=self.bg_color, height=20)
        spacer.pack(fill="x")

        # Header Title
        lbl_app_name = tk.Label(
            self, text="Student Management System",
            font=("Segoe UI", 15, "bold"), bg=self.bg_color, fg="#FFFFFF"
        )
        lbl_app_name.pack(pady=(15, 2))

        lbl_app_subtitle = tk.Label(
            self, text="Admission Guard Security Portal",
            font=("Segoe UI", 10), bg=self.bg_color, fg=self.text_secondary
        )
        lbl_app_subtitle.pack(pady=(0, 20))

        # Main Card Panel (White background)
        card = tk.Frame(self, bg=self.card_color, padx=25, pady=25,
                        highlightbackground=self.entry_border, highlightthickness=1, bd=0)
        card.pack(fill="both", expand=True, padx=25, pady=(0, 30))

        # Username Input
        lbl_user = tk.Label(
            card, text="Username", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_primary
        )
        lbl_user.pack(anchor="w", pady=(0, 5))

        self.entry_username = tk.Entry(
            card, font=("Segoe UI", 10),
            bg=self.entry_bg, fg=self.text_primary, insertbackground=self.text_primary,
            bd=0, highlightthickness=1, highlightbackground=self.entry_border, highlightcolor=self.primary_color
        )
        self.entry_username.pack(fill="x", ipady=6, pady=(0, 15))
        self.entry_username.focus()

        # Password Input
        lbl_pass = tk.Label(
            card, text="Password", font=("Segoe UI", 9, "bold"),
            bg=self.card_color, fg=self.text_primary
        )
        lbl_pass.pack(anchor="w", pady=(0, 5))

        self.entry_password = tk.Entry(
            card, font=("Segoe UI", 10), show="*",
            bg=self.entry_bg, fg=self.text_primary, insertbackground=self.text_primary,
            bd=0, highlightthickness=1, highlightbackground=self.entry_border, highlightcolor=self.primary_color
        )
        self.entry_password.pack(fill="x", ipady=6, pady=(0, 20))

        # Bind Enter keys to login execution
        self.entry_username.bind("<Return>", lambda e: self.perform_login())
        self.entry_password.bind("<Return>", lambda e: self.perform_login())

        # Login Button
        self.btn_login = tk.Button(
            card, text="Login", font=("Segoe UI", 11, "bold"),
            bg=self.primary_color, fg="#FFFFFF", relief="flat", bd=0,
            cursor="hand2", activebackground=self.hover_color, activeforeground="#FFFFFF",
            command=self.perform_login
        )
        self.btn_login.pack(fill="x", ipady=8)

        # Bind hover effects
        self.btn_login.bind("<Enter>", lambda e: self.btn_login.config(bg=self.hover_color))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.config(bg=self.primary_color))

    def perform_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Validation Warning", "All fields are required.")
            return

        try:
            if self.auth_service.authenticate(username, password):
                # Trigger callback and close
                self.on_success()
                self.destroy()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except StudentValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("System Error", f"An authentication error occurred: {e}")
