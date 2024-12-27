# Related third-party imports
import requests
from flask import Flask, jsonify, request
# local imports
from config import Config
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# define the scope
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

config = Config()

creds_dict = {
    "type": "service_account",
    "project_id": config.project_id,
    "private_key_id": config.private_key_id,
    "private_key": config.private_key,
    "client_email": config.client_email,
    "client_id": config.client_id,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": config.client_x509_cert_url,
    "universe_domain": "googleapis.com"
}

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict, scope)


# authorize the clientsheet
client = gspread.authorize(creds)

app = Flask(__name__)
config = Config()

today = date.today().isoformat()

ema_confluence = "@emaconfluence"
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
        if alertName == "emaconfluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={ema_confluence}&text={message}"
                print(requests.get(url).json())
                gsheet('emaconfluence', stockName)

        elif alertName == "pivot_ema_confluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={pivot_ema_confluence}&text={message}"
                # print(requests.get(url).json())
                gsheet('pivot_ema_confluence', stockName)
        elif alertName == "price_volume_analysis":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={price_volume_analysis}&text={message}"
                print(requests.get(url).json())
                gsheet('price_volume_analysis', stockName)
        elif alertName == "wklyvol_emaconfluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={wklyvol_emaconfluence}&text={message}"
                print(requests.get(url).json())
                gsheet("wklyvol_emaconfluence", stockName)
        elif alertName == "dlyvol_emaconfluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={dlyvol_emaconfluence}&text={message}"
                print(requests.get(url).json())
                gsheet("dlyvol_emaconfluence", stockName)
        elif alertName == "wklyvol_2times_6weeks":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={wklyvol_2times_6weeks}&text={message}"
                print(requests.get(url).json())
                gsheet("wklyvol_2times_6weeks", stockName)
        elif alertName == "dlyvol_2times_7days":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={dlyvol_2times_7days}&text={message}"
                print(requests.get(url).json())
                gsheet("dlyvol_2times_7days", stockName)

    except Exception as e:
        print(e)
        return jsonify({"status": 400, "message": "Something went wrong"})

    return jsonify({"status": 200, "message": "Alert Successfully"})


def gsheet(sheetName, list):
    sheet = client.open('Rajesh Sheety Alerts').worksheet(sheetName)
    cell = sheet.find(today)
    if cell:
        print("Column with today's date already exists.")
    else:
        sheet.insert_cols([None] * 1, col=2,
                          value_input_option='RAW', inherit_from_before=False)
        sheet.update_cell(1, 2, today)
    next_row = len(sheet.col_values(2)) + 1

    range_to_update = f'B{next_row}:B{next_row + len(list) - 1}'
    sheet.update([[value] for value in list], range_to_update)
    return jsonify({"status": 200, "message": "Alert Successfully"})


if __name__ == '__main__':
    app.run(debug=False)
