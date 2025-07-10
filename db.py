from flask_sqlalchemy import SQLAlchemy

# uninitialized instance of db;
# since many files will import db, we keep it in this
# separate file to avoid circular imports
db = SQLAlchemy()