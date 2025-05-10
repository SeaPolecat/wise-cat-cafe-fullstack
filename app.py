from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()

    app.logger.info("Starting Flask app...")

    app.run(debug=True, host='0.0.0.0', port=5002)