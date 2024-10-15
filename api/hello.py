from flask import Flask

# Flaskアプリのインスタンスを作成
app = Flask(__name__)

# ルートURLにアクセスしたときのルート処理
@app.route('/')
def hello():
    return 'Hello, World!'

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)