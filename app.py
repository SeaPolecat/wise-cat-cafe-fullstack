from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from utils import api_utils

from config import ProductionConfig

# uninitialized instance of db
db = SQLAlchemy()

def create_app(config_class=ProductionConfig):

    app = Flask(__name__)

    # configure database
    app.config.from_object(config_class)

    # initialize database
    db.init_app(app)

    # recreate all tables
    with app.app_context():
        db.create_all()

    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            img = api_utils.get_cat_image()

            # render template with variables
            return render_template('index.html', img=img)
        
            # return redirect('/')
        else:
            return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()

    app.logger.info("Starting Flask app...")

    app.run(debug=True, host='0.0.0.0', port=5002)