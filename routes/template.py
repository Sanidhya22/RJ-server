from flask import Blueprint, jsonify
from datetime import datetime
from pytz import timezone

template_bp = Blueprint('template', __name__)


@template_bp.route('/createTemplate', methods=['GET'])
def createTemplate():
    unformatted_date = datetime.now(timezone("Asia/Kolkata"))
    today = unformatted_date.strftime('%Y-%m-%d')
    try:
        sheet = template_bp.client.open('PIVOT BOSS SHEET')
        template_sheet = sheet.worksheet('Template FNO')

        # Create new sheet name with today's date
        new_sheet_name = f"{today} FNO"

        # Duplicate the template sheet
        sheet.duplicate_sheet(
            source_sheet_id=template_sheet.id,
            new_sheet_name=new_sheet_name
        )

        return jsonify({"status": 200, "message": f"Successfully created sheet: {new_sheet_name}"})

    except Exception as e:
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        return jsonify({"status": 400, "message": "Something went wrong"})


@template_bp.route('/createTemplateIndices', methods=['GET'])
def createTemplateIndices():
    unformatted_date = datetime.now(timezone("Asia/Kolkata"))
    today = unformatted_date.strftime('%Y-%m-%d')
    try:
        sheet = template_bp.client.open('PIVOT BOSS SHEET')
        template_sheet = sheet.worksheet('Template INDICES')

        # Create new sheet name with today's date
        new_sheet_name = f"{today} Indices"

        # Duplicate the template sheet
        sheet.duplicate_sheet(
            source_sheet_id=template_sheet.id,
            new_sheet_name=new_sheet_name
        )

        return jsonify({"status": 200, "message": f"Successfully created sheet: {new_sheet_name}"})

    except Exception as e:
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        return jsonify({"status": 400, "message": "Something went wrong"})
