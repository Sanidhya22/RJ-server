from flask import Blueprint, jsonify
from datetime import datetime
from pytz import timezone
import gspread

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/updateDashboard', methods=['GET'])
def updateDashboard():
    unformatted_date = datetime.now(timezone("Asia/Kolkata"))
    today = unformatted_date.strftime('%Y-%m-%d')
    try:
        sheet = dashboard_bp.client.open('Rajesh Shetty Alerts')
        dashboardSheet = sheet.worksheet('Dashboard')
        dashboardSheet.update_cell(2, 16, today)
        range_to_clear = f'A2:{gspread.utils.rowcol_to_a1(250, 15)}'
        dashboardSheet.batch_clear([range_to_clear])

        return jsonify({"status": 200, "message": 'Dashboard updated successfully'})

    except Exception as e:
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        return jsonify({"status": 400, "message": "Failed to update dashboard"})
