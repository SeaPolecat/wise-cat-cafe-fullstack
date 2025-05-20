from app import db

from datetime import datetime, timezone

class Cat(db.Model):

    id = db.Column(db.Integer, primay_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String, nullable=False)
    wisdom = db.Column(db.String, nullable=False)
    date_summoned = db.Column(db.DateTime)

    def __repr__(self):
        return f'{self.id}) {self.name}. Summoned on {self.date_summoned}.'
    
    def __init__(self):
        self.name = ''
        # self.image = api call
        # self.wisdom = api call
        self.date_summoned = datetime.now(timezone.utc)
