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
    def find_user_by_username(username: str) -> 'User':
        """Given a username, finds and returns the corresponding user from the database.
        """
        # ilike ignores case (must use with filter, not filter_by)
        return User.query.filter(User.username.ilike(username)).first()


    @classmethod
    def find_signup_errors(cls, username: str, password: str, confirmed_pass: str) -> dict[str, str]:
        """Finds errors within the given signup data.
        """
        errors = {}

        if cls.find_user_by_username(username=username):
            errors['username_error'] = "Sorry, that username is taken"

        elif len(password) < 10:
            errors['password_error'] = "Password must be at least 10 characters long"
            
        elif ' ' in password:
            errors['password_error'] = "Password cannot contain spaces"

        elif confirmed_pass != password:
            errors['confirmed_pass_error'] = "This did not match the password above"

        return errors
    

    @classmethod
    def is_password_correct(cls, hashed_password: str, password: str) -> bool:
        """Unhashes the hashed_password and checks if it matches the given password.
        """
        if not check_password_hash(hashed_password, password):
            return False

        return True
    

    @classmethod
    def create_user(cls, username: str, password: str) -> None:
        """Creates a new user to add to the database.
        """
        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()