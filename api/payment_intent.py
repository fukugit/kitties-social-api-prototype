from flask import Flask,Blueprint, request,current_app, jsonify
import stripe
import os

# Flaskアプリケーションを作成
app = Flask(__name__)

payment_intent_bp = Blueprint('payment_intent', __name__, url_prefix='/payment_intent')


@payment_intent_bp.route('/createpaymentintent', methods=['POST'])
def createpaymentintent():


    # Stripe秘密鍵の設定
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    try:
        # リクエストデータを取得
        data = request.get_json()
        if not data or 'amount' not in data:
            return jsonify({"error": "Amount is required"}), 400

        # PaymentIntentを作成
        payment_intent = stripe.PaymentIntent.create(
            amount=data['amount'],  # 金額（単位: 最小通貨単位）
            currency=data['currency'],         # 通貨コード
            payment_method_types=[data['payment_method_types']]  # サポートする支払い方法
        )

        # client_secretをフロントエンドに返す
        return jsonify({'status': 'ok',
                    'error_message': '',
                    'data': {
                        'clientSecret': payment_intent['client_secret']
                    }}), 200

    except stripe.error.StripeError as e:
        # Stripeエラーの処理
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # その他のエラーの処理
        return jsonify({"error": "Server error: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
