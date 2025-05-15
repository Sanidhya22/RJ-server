from flask import Blueprint, jsonify, request
import requests
from datetime import datetime
from pytz import timezone

telegram_bp = Blueprint('telegram', __name__)

# Chat IDs mapping
CHAT_IDS = {
    "PURE ONLY CPR": "@PURE_ONLY_CPR",
    "D/W NARROW CPR": "@D_W_NARROW_CPR",
    "W/M NARROW CPR": "@W_M_CPR",
    "ema_confluence": "@ema_confluence",
    "pivot_ema_confluence": "@pivot_ema_confluence",
    "price_volume_analysis": "@price_volume_analysis",
    "wklyvol_emaconfluence": "@wklyvol_emaconfluence",
    "dlyvol_emaconfluence": "@dlyvol_emaconfluence",
    "wklyvol_2times_6weeks": "@wklyvol_2times_6weeks",
    "dlyvol_2times_7days": "@dlyvol_2times_7days",
    "CPR_POC_CASH": "@CPR_POC_CASH",
    "CPR_POC_FNO": "@CPR_POC",
    "NARROW D/W/M CPR": "@NARROW_CPR",
    "INSIDECAMERILLA": "@inside_camerilla"
}


def gsheet(sheetName, list):
    sheet = telegram_bp.client.open('Rajesh Shetty Alerts')
    sheetOne = sheet.worksheet(sheetName)
    dashboardSheet = sheet.worksheet('Dashboard')
    next_row = len(sheetOne.col_values(3)) + 1
    range_to_update = f'C{next_row}:C{next_row + len(list) - 1}'

    sheetOne.update([[value] for value in list], range_to_update)

    column_map = {
        'PURE ONLY CPR': 'A',
        'D/W NARROW CPR': 'B',
        'W/M NARROW CPR': 'C',
        'ema_confluence': 'I',
        'pivot_ema_confluence': 'H',
        'price_volume_analysis': 'G',
        'wklyvol_emaconfluence': 'K',
        'dlyvol_emaconfluence': 'J',
        'wklyvol_2times_6weeks': 'M',
        'dlyvol_2times_7days': 'L',
        'CPR_POC_FNO': 'E',
        'CPR_POC_CASH': 'F',
        'NARROW D/W/M CPR': 'D',
        'INSIDECAMERILLA': 'N'
    }

    print(f"Updating {sheetName} sheet")

    if sheetName in column_map:
        print(f"Updating dashboard sheet for {sheetName}")
        col_letter = column_map[sheetName]
        range_to_update_dashboard = f'{col_letter}{next_row}:{col_letter}{next_row + len(list) - 1}'
        dashboardSheet.update([[value] for value in list],
                              range_to_update_dashboard)

    return jsonify({"status": 200, "message": "Alert Successfully"})


@telegram_bp.route('/telegramWekhook', methods=['POST'])
def telegramAlertShort():
    try:
        stocksData = request.json.get('stocks')
        triggerPriceData = request.json.get('trigger_prices')
        alertName = request.json.get('alert_name')
        place_at = [float(o.strip()) for o in triggerPriceData.split(',')]
        stockName = [o.strip() for o in stocksData.split(',')]

        if alertName in CHAT_IDS:
            chat_id = CHAT_IDS[alertName]
            for tradingsymbol, execute_at in zip(stockName, place_at):
                message = f"{tradingsymbol} \nPrice={execute_at}"
                url = f"https://api.telegram.org/bot{telegram_bp.config.telegram_bot_token}/sendMessage?chat_id={chat_id}&text={message}"
                print(requests.get(url).json())
            print(f"Updating dashboard sheet for {alertName}")
            gsheet(alertName, stockName)

    except Exception as e:
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        return jsonify({"status": 400, "message": "Something went wrong"})

    return jsonify({"status": 200, "message": "Alert Successfully"})
