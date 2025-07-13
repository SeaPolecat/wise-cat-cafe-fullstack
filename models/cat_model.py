from flask import session

from db import db

from datetime import datetime, timezone

class Cat(db.Model):

    __tablename__ = 'cats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String, nullable=False)
    wisdom = db.Column(db.String, nullable=False)
    date_summoned = db.Column(db.DateTime)

    def __repr__(self):
        return f'{self.id}) {self.name}. Summoned on {self.date_summoned.date()}.'
    
    def __init__(self, image: str, wisdom: str):
        self.name = ''
        self.image = image
        self.wisdom = wisdom
        self.date_summoned = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, any]:
        return {
            'name': self.name,
            'image': self.image,
            'wisdom': self.wisdom,
            'date_summoned': self.date_summoned
        }
    
    @classmethod
    def to_cat(cls, data: dict[str, any]) -> 'Cat':
        cat = Cat(image=data['image'], wisdom=data['wisdom'])

        cat.name = data['name']
        cat.date_summoned = data['date_summoned']

        return cat
    

    @classmethod
    def summon_cat(cls, img: str, wisdom: str) -> None:
        new_cat = Cat(img, wisdom)

        # store a cache of cats in the flask session, 
        # a dict that's unique to each user

        if not session.get('cache'):
            session['cache'] = [new_cat.to_dict()] # turn object to dict, because session can only store JSON values

        else:
            # session vars are immutable, so we must 
            # make a new cache every time
            cache = session['cache']

            cache.insert(0, new_cat.to_dict())

            # limit cache size to 2
            if len(cache) > 2:
                cache.pop(-1)

            session['cache'] = cache


    @classmethod
    def adopt_cat(cls, name: str) -> None:
        cat = Cat.to_cat(session.get('cache')[0])

        cat.name = name

        db.session.add(cat)
        db.session.commit()

        session.get('cache').pop(0)