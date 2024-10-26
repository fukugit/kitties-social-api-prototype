from flask import jsonify

from config import app, db
from model import Cat


@app.route('/')
def hello():
    hello = {
        'greeting': "Hello World!"
    }
    return jsonify(hello)

@app.route('/get-all-cat')
def get_all_cat():
    cats = db.session.query(Cat)
    cats_data = [
        {
            "id": cat.id,
            "name": cat.name,
            "breed": cat.breed,
            "created_at": cat.created_at
        } for cat in cats
    ]
    return jsonify(cats_data)

if __name__ == '__main__':
    app.run(debug=True)