"""
MIT License

Copyright (c) 2024 CNN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import hmac
import hashlib
import base64
from urllib.parse import parse_qs
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"  # Replace with your actual bot token


# Credit : https://gist.github.com/konstantin24121/49da5d8023532d66cc4db1136435a885?permalink_comment_id=5151548#gistcomment-5151548
def verify_telegram_web_app_data(telegram_init_data):
    init_data = parse_qs(telegram_init_data)
    hash_value = init_data.get('hash', [None])[0]
    data_to_check = []

    # Sort key-value pairs alphabetically
    sorted_items = sorted((key, val[0]) for key, val in init_data.items() if key != 'hash')
    data_to_check = [f"{key}={value}" for key, value in sorted_items]

    # HMAC Calculation
    secret = hmac.new(b"WebAppData", TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256).digest()
    _hash = hmac.new(secret, "\n".join(data_to_check).encode(), hashlib.sha256).hexdigest()

    # Verify hash matches
    if _hash == hash_value:
        return init_data.get('user', [None])[0], None
    else:
        return None, "Invalid hash"
# ==================================================================================

# Decorator to require authentication
def require_authentication(f):
    def wrapper(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization required"}), 401

        # Decode the base64 token
        token = auth_header.split(" ")[1]
        try:
            decoded_token = base64.b64decode(token).decode()
        except Exception as e:
            return jsonify({"error": "Token decoding failed"}), 401

        # Verify Telegram Web App data
        user, error = verify_telegram_web_app_data(decoded_token)
        if error:
            return jsonify({"error": error}), 401
        if not user:
            return jsonify({"error": "User not authenticated"}), 401
        return f(user, *args, **kwargs)
    
    wrapper.__name__ = f.__name__
    return wrapper


@app.route("/", methods=["GET"])
@require_authentication
def index(user):
    return jsonify({
        'message': 'TMA AUTH WITH FLASK',
        'user': user
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
