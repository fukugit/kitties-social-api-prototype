from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    hello = {
        'greeting': "Hello World!"
    }
    return jsonify(hello)

if __name__ == '__main__':
    app.run(debug=True)