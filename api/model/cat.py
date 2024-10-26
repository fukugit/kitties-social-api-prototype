from datetime import datetime

from api.config import db

class Cat (db.Model):
    __tablename__ = 'cat_information'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    breed = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, id, name, breed, created_at):
        self.id = id
        self.name = name
        self.breed = breed
        self.created_at = created_at

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, breed={self.breed}, created_at={self.created_at})>"