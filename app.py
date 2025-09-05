import os

from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from utils import api_utils

from config import ProductionConfig

from db import db
from models.cat_model import Cat
from models.user_model import User

def create_app(config_class=ProductionConfig):

    app = Flask(__name__)

    # configure database
    app.config.from_object(config_class)

    # initialize database
    db.init_app(app)

    # recreate all tables
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()

    # set up login manager
    login_manager.init_app(app)

    # determine where to redirect if a login is needed
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(username):
        return User.find_user_by_username(username)


    @app.route('/', methods=['GET'])
    def index():
        return redirect('/home')
    

    @app.route('/home', methods=['GET'])
    def home():
        return render_template('home.html')
    
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if current_user.is_authenticated:
            return redirect('/home')
        
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirmed_pass = request.form['confirm_password']

            errors = User.find_signup_errors(username=username, password=password, confirmed_pass=confirmed_pass)

            if errors:
                # **errors unpacks the errors dict, turning each key-val into a separate parameter.
                # pass username so the user doesn't need to re-enter it
                return render_template('signup.html', username=username, **errors)
            
            User.create_user(username=username, password=password)

            signup_success = "Account created successfully! You can now log in"

            return render_template('login.html', signup_success=signup_success)

        return render_template('signup.html')
    

    @app.route('/login', methods=['GET', 'POST'])
    def login(): # named 'login' because login_manager.login_view == 'login'
        if current_user.is_authenticated:
            return redirect('/home')

        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.find_user_by_username(username)

            if not user or not User.is_password_correct(user.hashed_password, password):
                login_error = "The username or password was incorrect"
                
                return render_template('login.html', username=username, login_error=login_error)

            # login_user stores whatever user.get_id() returns into the Flask session as '_user_id';
            # it's then used by the default Flask user_loader above
            login_user(user)
            
            return redirect('/home')

        return render_template('login.html')
    

    @app.route('/logout', methods=['GET'])
    @login_required
    def logout():
        """Logs out the user.
        """
        logout_user()

        return redirect('/home')


    @app.route('/summon', methods=['GET'])
    @login_required
    def summon():
        img = api_utils.get_cat_image()
        wisdom = api_utils.get_wisdom()

        Cat.summon_cat(img=img, wisdom=wisdom)

        # render template with variables
        return render_template('summon.html', img=img, wisdom=wisdom)
    

    @app.route('/adopt', methods=['GET', 'POST'])
    @login_required
    def adopt():
        if request.method == 'POST':
            name = request.form['name']

            Cat.adopt_cat(name=name)
            
        return redirect('/home')

    
    return app

if __name__ == '__main__':
    app = create_app()

    app.logger.info("Starting Flask app...")

    app.run(debug=True, host='0.0.0.0', port=5002)