from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    hello = {
        'greeting': "Hello World!"
    }
    return jsonify(hello)

if __name__ == '__main__':
    app.run(debug=True)