from db import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(32), nullable=False)  # 16-byte salt in hex
    password = db.Column(db.String(64), nullable=False)  # SHA-256 hash in hex


    @staticmethod
    def is_duplicate_username(username: str) -> bool:
        """Checks if a user with the given username already exists in the database.
        """
        return False


    @classmethod
    def find_signup_errors(cls, username: str, password: str, confirmed_pass: str) -> dict[str, str]:
        """Finds errors within the given signup data.
        """
        errors = {}

        if cls.is_duplicate_username(username=username):
            errors['username_error'] = "Username already exists"

        elif len(password) < 10:
            errors['password_error'] = "Password must be at least 10 characters long"
            
        elif ' ' in password:
            errors['password_error'] = "Password cannot contain spaces"

        elif confirmed_pass != password:
            errors['confirmed_pass_error'] = "This did not match the password above"

        return errors