from datetime import datetime, timezone, timedelta

from flask import jsonify


def create_response(data=None, message="success", code=0, http_status=200):
    response = {
        "code": code,
        "message": message,
        "data": data,
        "timestamp": datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(response), http_status