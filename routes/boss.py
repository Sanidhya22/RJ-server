from flask import Blueprint, jsonify, request
from datetime import datetime
from pytz import timezone

boss_bp = Blueprint('boss', __name__)


@boss_bp.route('/bossSheetFno', methods=['POST'])
def bossSheet():
    try:
        stocksData = request.json.get('stocks')
        alertName = request.json.get('alert_name')
        stockNames = [o.strip() for o in stocksData.split(',')]

        # Get today's date sheet
        unformatted_date = datetime.now(timezone("Asia/Kolkata"))
        today = unformatted_date.strftime('%Y-%m-%d')
        sheet = boss_bp.client.open('PIVOT BOSS SHEET')
        worksheet = sheet.worksheet(f"{today} FNO")

        # Get all stock cells from column A once
        stock_cells = worksheet.range('A1:A1000')  # Adjust range as needed
        stock_dict = {
            cell.value: cell.row for cell in stock_cells if cell.value}

        # Handle single column alerts
        single_column_alerts = {
            'MTF.CPR': 'E',
            'BASIC': 'F'
        }

        updates = []  # List to store all cell updates

        if alertName in single_column_alerts:
            target_col = single_column_alerts[alertName]
            col_num = ord(target_col) - ord('A') + 1

            for stock in stockNames:
                if stock in stock_dict:
                    cell = f'{target_col}{stock_dict[stock]}'
                    updates.append({
                        'range': cell,
                        'values': [['YES']]
                    })

        else:
            category, timeframe = alertName.split('_')

            category_columns = {
                'NRCPR': {'start': 'G', 'end': 'I'},
                'IN.CAM': {'start': 'J', 'end': 'L'},
                'GPZ': {'start': 'M', 'end': 'O'}
            }

            timeframe_offset = {'D': 0, 'W': 1, 'M': 2}

            if category in category_columns:
                base_col = category_columns[category]['start']
                target_col = chr(ord(base_col) + timeframe_offset[timeframe])

                for stock in stockNames:
                    if stock in stock_dict:
                        cell = f'{target_col}{stock_dict[stock]}'
                        updates.append({
                            'range': cell,
                            'values': [['YES']]
                        })

        # Perform batch update if there are any updates
        if updates:
            worksheet.batch_update(updates)

        return jsonify({"status": 200, "message": "Sheet updated successfully"})

    except Exception as e:
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        return jsonify({"status": 400, "message": "Something went wrong"})


@boss_bp.route('/bossSheetIndices', methods=['POST'])
def bossSheetIndicesS():
    try:
        stocksData = request.json.get('stocks')
        alertName = request.json.get('alert_name')
        stockNames = [o.strip() for o in stocksData.split(',')]

        # Get today's date sheet
        unformatted_date = datetime.now(timezone("Asia/Kolkata"))
        today = unformatted_date.strftime('%Y-%m-%d')
        sheet = boss_bp.client.open('PIVOT BOSS SHEET')
        worksheet = sheet.worksheet(f"{today} Indices")

        # Get all stock cells from column A once
        stock_cells = worksheet.range('A1:A1000')  # Adjust range as needed
        stock_dict = {
            cell.value: cell.row for cell in stock_cells if cell.value}

        # Handle single column alerts
        single_column_alerts = {
            'MTF.CPR': 'B',
            'BASIC': 'C'
        }

        updates = []  # List to store all cell updates

        if alertName in single_column_alerts:
            target_col = single_column_alerts[alertName]
            col_num = ord(target_col) - ord('A') + 1

            for stock in stockNames:
                if stock in stock_dict:
                    cell = f'{target_col}{stock_dict[stock]}'
                    updates.append({
                        'range': cell,
                        'values': [['YES']]
                    })

        else:
            category, timeframe = alertName.split('_')

            category_columns = {
                'NRCPR': {'start': 'D', 'end': 'F'},
                'IN.CAM': {'start': 'G', 'end': 'I'},
                'GPZ': {'start': 'J', 'end': 'L'}
            }

            timeframe_offset = {'D': 0, 'W': 1, 'M': 2}

            if category in category_columns:
                base_col = category_columns[category]['start']
                target_col = chr(ord(base_col) + timeframe_offset[timeframe])

                for stock in stockNames:
                    if stock in stock_dict:
                        cell = f'{target_col}{stock_dict[stock]}'
                        updates.append({
                            'range': cell,
                            'values': [['YES']]
                        })

        # Perform batch update if there are any updates
        if updates:
            worksheet.batch_update(updates)

        return jsonify({"status": 200, "message": "Sheet updated successfully"})

    except Exception as e:
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        return jsonify({"status": 400, "message": "Something went wrong"})
