from datetime import datetime

from api import db

class Cat (db.Model):
    """
    テスト用モデルです．
    """
    __tablename__ = 'cat_information'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    breed = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, breed={self.breed}, created_at={self.created_at})>"