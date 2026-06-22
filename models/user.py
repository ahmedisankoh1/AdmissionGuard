from utils.validators import StudentValidationError

class User:
    """
    Represents a system user entity for authentication.
    """

    def __init__(self, username, password, user_id=None):
        self.user_id = user_id
        self.username = username
        self.password = password

    def create_user(self, db_manager):
        """
        Saves a new user to the database.
        """
        if not self.username or not str(self.username).strip():
            raise StudentValidationError("Username cannot be empty.")
        if not self.password or not str(self.password).strip():
            raise StudentValidationError("Password cannot be empty.")

        username_cleaned = str(self.username).strip()
        
        # Check if username already exists
        dup_query = "SELECT COUNT(*) FROM users WHERE username = ?;"
        dup_check = db_manager.fetch_one(dup_query, (username_cleaned,))
        if dup_check and dup_check[0] > 0:
            raise StudentValidationError(f"Username '{username_cleaned}' already exists.")

        query = "INSERT INTO users (username, password) VALUES (?, ?);"
        params = (username_cleaned, self.password)
        self.user_id = db_manager.execute_query(query, params)
        return self.user_id

    @staticmethod
    def get_user(db_manager, username):
        """
        Fetches a user from the database by username.
        """
        if not username or not str(username).strip():
            return None

        query = "SELECT user_id, username, password FROM users WHERE username = ?;"
        row = db_manager.fetch_one(query, (str(username).strip(),))
        if row:
            return User(user_id=row[0], username=row[1], password=row[2])
        return None

    def validate_user(self, password):
        """
        Validates the user's password.
        """
        return self.password == password

    def __repr__(self):
        return f"User({self.user_id}, '{self.username}')"
