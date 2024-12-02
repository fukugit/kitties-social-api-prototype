from datetime import datetime

from api import db

class Pedigree (db.Model):
    """
    テスト用モデルです．
    """
    __tablename__ = 'pedigree'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, nullable=False)
    upload_user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_program = db.Column(db.String(255), nullable=False)
    updated_program = db.Column(db.String(255), nullable=False)
    deleted_program = db.Column(db.String(255))
    deleted_at = db.Column(db.DateTime)
    file_name = db.Column(db.String(255), nullable=False)

    def __init__(self, cat_id, upload_user_id, file_name):
        self.cat_id = cat_id
        self.upload_user_id = upload_user_id
        self.created_program = "Flask"
        self.updated_program ="Flask"
        self.file_name = file_name

    def __repr__(self):
        return f"<Pedigree(id={self.id}>"