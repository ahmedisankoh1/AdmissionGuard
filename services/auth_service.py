from models.user import User
from utils.validators import StudentValidationError

class AuthService:
    """
    AuthService handles system authentication, default admin user checks/creation, 
    and session management.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.current_user = None
        
        # Automatically create default admin if needed
        self.create_default_admin()

    def authenticate(self, username, password):
        """
        Validates username and password against the database.
        Sets current_user on success, returns True. Returns False on failure.
        """
        if not username or not str(username).strip():
            raise StudentValidationError("Username is required.")
        if not password:
            raise StudentValidationError("Password is required.")

        user = User.get_user(self.db_manager, username)
        if user and user.validate_user(password):
            self.current_user = user
            return True
        return False

    def create_default_admin(self):
        """
        Automatically inserts default admin account if no users exist in the database.
        """
        query = "SELECT COUNT(*) FROM users;"
        try:
            row = self.db_manager.fetch_one(query)
            if row and row[0] == 0:
                admin_user = User(username="admin", password="admin123")
                admin_user.create_user(self.db_manager)
                print("Default administrator ('admin') created automatically.")
        except Exception as e:
            print(f"Failed to check/create default admin: {e}")

    def logout(self):
        """
        Clears the current active session.
        """
        self.current_user = None
