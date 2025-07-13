import os

from flask import Flask, render_template, request, redirect
from utils import api_utils

from config import ProductionConfig

from db import db
from models.cat_model import Cat

def create_app(config_class=ProductionConfig):

    app = Flask(__name__)

    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    # configure database
    app.config.from_object(config_class)

    # initialize database
    db.init_app(app)

    # recreate all tables
    with app.app_context():
        db.create_all()


    @app.route('/', methods=['GET'])
    def index():
        return redirect('/home')
    

    @app.route('/home', methods=['GET'])
    def home():
        return render_template('index.html', hide_adopt=True)


    @app.route('/summon', methods=['GET'])
    def summon():
        img = api_utils.get_cat_image()
        wisdom = api_utils.get_wisdom()

        Cat.summon_cat(img=img, wisdom=wisdom)

        # render template with variables
        return render_template('index.html', img=img, wisdom=wisdom, hide_summon=True)
    

    @app.route('/adopt', methods=['GET', 'POST'])
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