# Related third-party imports
import requests
from flask import Flask, jsonify, request
# local imports
from config import Config

app = Flask(__name__)
config = Config()

ema_confluence = "@onlyemaconfluence"
pivot_ema_confluence = "@pivot_ema_confluence"

price_volume_analysis = '@price_volume_analysis'
wklyvol_emaconfluence = '@wklyvol_emaconfluence'
dlyvol_emaconfluence = '@dlyvol_emaconfluence'
wklyvol_2times_6weeks = '@wklyvol_2times_6weeks'
dlyvol_2times_7days = '@dlyvol_2times_7days'


@app.route('/telegramWekhook', methods=['POST'])
def telegramAlertShort():
    try:
        stocksData = request.json.get('stocks')
        triggerPriceData = request.json.get('trigger_prices')
        alertName = request.json.get('alert_name')
        place_at = [float(o.strip())
                    for o in triggerPriceData.split(',')]
        stockName = [o for o in stocksData.split(',')]
        if alertName == "onlyemaconfluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={ema_confluence}&text={message}"
                print(requests.get(url).json())

        elif alertName == "pivot_ema_confluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={pivot_ema_confluence}&text={message}"
                print(requests.get(url).json())
        elif alertName == "price_volume_analysis":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={price_volume_analysis}&text={message}"
                print(requests.get(url).json())
        elif alertName == "wklyvol_emaconfluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={wklyvol_emaconfluence}&text={message}"
                print(requests.get(url).json())
        elif alertName == "dlyvol_emaconfluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={dlyvol_emaconfluence}&text={message}"
                print(requests.get(url).json())
        elif alertName == "wklyvol_2times_6weeks":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={wklyvol_2times_6weeks}&text={message}"
                print(requests.get(url).json())
        elif alertName == "dlyvol_2times_7days":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={dlyvol_2times_7days}&text={message}"
                print(requests.get(url).json())

    except Exception as e:
        print(e)
        return jsonify({"status": 400, "message": "Something went wrong"})

    return jsonify({"status": 200, "message": "Alert Successfully"})


if __name__ == '__main__':
    app.run(debug=False)
