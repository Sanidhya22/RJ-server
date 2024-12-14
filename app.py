# Standard library imports
from urllib.parse import urlparse, parse_qs
# Related third-party imports
import requests
from flask import Flask, jsonify
# local imports
from config import Config

app = Flask(__name__)
config = Config()


@app.route('/telegramWekhook', methods=['POST'])
def telegramAlertShort():
    try:

        # stocksData = request.json.get('stocks')
        # triggerPriceData = request.json.get('trigger_prices')
        message = f"testsdtsadad"
        url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={config.telegram_channel_id}&text={message}"
        print(requests.get(url).json())
    except Exception as e:
        print(e)

    return jsonify({"status": 200, "message": "Alert Successfully"})


if __name__ == '__main__':
    app.run(debug=False)
