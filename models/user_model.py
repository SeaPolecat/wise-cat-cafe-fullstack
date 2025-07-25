from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.hashed_password = generate_password_hash(password)


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
    

    @classmethod
    def create_user(cls, username: str, password: str) -> None:
        """Creates a new user to add to the database.
        """
        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()