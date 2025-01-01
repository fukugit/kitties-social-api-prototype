from flask import Flask, request,current_app, jsonify
from flask import Blueprint
import stripe

# Flaskアプリケーションを作成
app = Flask(__name__)

stripe_bp = Blueprint('stripe', __name__, url_prefix='/stripe')

@stripe_bp.route('/createproduct', methods=['POST'])
def createproduct():

    # Stripeのシークレットキーを設定
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    try:
        # リクエストデータを取得
        data = request.json
        name = data.get("name")
        price = data.get("price")  # 単位はセント（100セント = 1ドル）

        # 商品を作成
        product = stripe.Product.create(
            name=name
        )

        # 価格を作成
        price_obj = stripe.Price.create(
            unit_amount=price,
            currency="usd",  # 通貨を指定
            product=product['id']
        )

        return jsonify({
            "product": product,
            "price": price_obj
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# BlueprintをFlaskアプリに登録
app.register_blueprint(stripe_bp)

if __name__ == '__main__':
    app.run(debug=True)