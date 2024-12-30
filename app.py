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
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDXaaHpduS8I5K\nMXUCZatlCUwgL6nXXtlGh3IK8/l2/s51q/wNK1pIxb2+6+cL6I331urZfk89/pp0\nTa0zYKyljH55UBpbF6MkbwFueR4uiYXNDBm4a658sbP7mutTG0QV3NSol6VsRo6a\nwxxhLYOuroT+UYxEA4FbVR4BpXkKmM5qHFmX/PdKz4Y+7qzXxDlRZs3dbI00q8w9\nWuVBxnC9VOs7T8d0LgXb6pMrdUbOeZ5EAjfhjLSgrOhBvoSy7vEtUItlEnLYnLE +\nr7louyBcqdF2VjMtiJ1OPhGu3K/Z6oXtczQpaPYOotD0/ktupov2rspjoGB18VGy\ntNr6EmcFAgMBAAECggEAD/URShkhAzKE3MiHXyfAxSLqReK+w6mqo5kiloRxBugv\nIutmTgkReco1AmgwWgenuOukCRnJDS5DnWZO1Fh8IZWFKxGA5ZnbqHksq8JW1cRD\n2oi3fRnGicbWBaIUwJgEiqib8h1Y1Kw6r6dqJQHbtKPqlv9ALrn+keA08Dt81IGc\nIDe3rqL3nDzFuHHCr35EZvlWzmRU907GrAHftSkdQTEOJNDqrrg2BYkW+tqewhRl\n8csMlqA08cNng1Ni6InC6gkfGverx9GRN+QHb8+9In4cQlEAi1+ps5M94sWHHJib\nqzx5eUpIdTaNAO0zHdoDfCmkxl15nOS7DdzG0zODrQKBgQDqFZi4o6sDKyzMmU9m\n/F7f/wi9d2eal+yI62PBQNmvI0IkIk1IjUf4HCkA6/8AoIdYoJU7uGZI3TIkfW3r\nsPDHgDjd8NRUPB6WHtmwVkFf7a1IF8XxbWi/Wtt4mjVdNCME/KO7T2ElZNBsQDZ6\nf0nOFzs/EEc+B2y75P38le5d7wKBgQDVqBHQL+zXtN/9Ql12GVRsoYcns5Uqrcjg\nYibJYEswJ87N5RIDucIaSny6eGQq4vOP5jxUga5ztCjIIbgf7AJ+PPG/JQJynTF9\nnoJUETlJuWNqyid7XCnDTTNfvU7OjX+QcWbAjPNPkEiaY6lyMaO+Y/brNinvAO //\n5VjpAlM+SwKBgQCXLQ1tqV3ndPnAxP5Pv4syVI37duL1J0q+fm71PwGXJ0ku9uw8\nf+nL5bvheYg9im7+oO7gG84LHrekc1ELF0HZRgjz5PXr1MvYHeJvDLW501DGr3vJ\n2OP+ORpmgAkYwXQgY10GulQ+BybH0oycfhpXPA+qQcQQ3lCt5EzX1KiWBwKBgQCD\neDsV1xevF/6ocZjfHfEEM1TeSjPkojE0WVEyow1BIY2wxl8SadCVqvYbLA+/EA39\noxfGjFHToq1hkNYi1nAmS8wZ6WUbL70PZmUd48dTpT8WrDQlRW3xXmTZaby/fvRa\n5lzq6RCjCc6TKfZPbVorwoli7N5a0kHcPb07DBI7BwKBgGZBnVaUnxqdQtcNWMoH\nYprWsuJz+sYz73ANb38NB5qyzGjdZ1xikTGCDDs5JK5p8uPnf/73uZkQG8u/1Xo6\nmxU5Ff5M55PYthuuL7bpKUeS9lE6rqS9f/rNMOncoEjPp6qrnzDEsfZ/ehzbDYDV\nUqxVQIpdMLsRLma9g/W8C7C /\n-----END PRIVATE KEY-----\n",
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

ema_confluence = "@ema_confluence"
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
        if alertName == "ema_confluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={ema_confluence}&text={message}"
                print(requests.get(url).json())
            gsheet('ema_confluence', stockName)

        elif alertName == "pivot_ema_confluence":
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage?chat_id={pivot_ema_confluence}&text={message}"
                print(requests.get(url).json())
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
    sheet = client.open('Rajesh Sheety Alerts')
    sheetOne = sheet.worksheet(sheetName)
    sheetTwo = sheet.worksheet('Dashboard')
    cell = sheetOne.find(today)
    if cell:
        print("Column with today's date already exists.")
    else:
        sheetOne.insert_cols([None] * 1, col=3,
                             value_input_option='RAW', inherit_from_before=False)
        sheetOne.update_cell(1, 3, today)
    next_row = len(sheetOne.col_values(3)) + 1

    range_to_update = f'C{next_row}:C{next_row + len(list) - 1}'
    sheetOne.update([[value] for value in list], range_to_update)

    if sheetName == 'ema_confluence':
        range_to_update = f'A{next_row}:A{next_row + len(list) - 1}'
        sheetTwo.update([[value] for value in list], range_to_update)

    if sheetName == 'pivot_ema_confluence':
        range_to_update = f'B{next_row}:B{next_row + len(list) - 1}'
        sheetTwo.update([[value] for value in list], range_to_update)

    if sheetName == 'price_volume_analysis':
        range_to_update = f'C{next_row}:C{next_row + len(list) - 1}'
        sheetTwo.update([[value] for value in list], range_to_update)

    if sheetName == 'wklyvol_emaconfluence':
        range_to_update = f'D{next_row}:D{next_row + len(list) - 1}'
        sheetTwo.update([[value] for value in list], range_to_update)

    if sheetName == 'dlyvol_emaconfluence':
        range_to_update = f'E{next_row}:E{next_row + len(list) - 1}'
        sheetTwo.update([[value] for value in list], range_to_update)
    if sheetName == 'wklyvol_2times_6weeks':
        range_to_update = f'F{next_row}:F{next_row + len(list) - 1}'
        sheetTwo.update([[value] for value in list], range_to_update)

    if sheetName == 'dlyvol_2times_7days':
        range_to_update = f'G{next_row}:G{next_row + len(list) - 1}'
        sheetTwo.update([[value] for value in list], range_to_update)

    return jsonify({"status": 200, "message": "Alert Successfully"})


if __name__ == '__main__':
    app.run(debug=False)
