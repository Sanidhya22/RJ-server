from flask import Blueprint, jsonify
from datetime import datetime
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

sheet_bp = Blueprint('sheet', __name__)


@sheet_bp.route('/updateSheets', methods=['GET'])
def updateSheets():
    unformatted_date = datetime.now(timezone("Asia/Kolkata"))
    today = unformatted_date.strftime('%Y-%m-%d')
    try:
        sheet = sheet_bp.client.open('Rajesh Shetty Alerts')
        sheets = [
            "PURE ONLY CPR",
            "D/W NARROW CPR",
            "W/M NARROW CPR",
            "ema_confluence",
            "pivot_ema_confluence",
            "price_volume_analysis",
            "wklyvol_emaconfluence",
            "dlyvol_emaconfluence",
            "wklyvol_2times_6weeks",
            "dlyvol_2times_7days",
            'CPR_POC_CASH',
            'CPR_POC_FNO',
            'NARROW D/W/M CPR',
            "INSIDECAMERILLA"
        ]

        def update_single_sheet(sheet_name):
            try:
                tempSheet = sheet.worksheet(sheet_name)

                # Batch operations instead of individual calls
                batch_updates = [
                    {
                        'insertDimension': {
                            'range': {
                                'sheetId': tempSheet.id,
                                'dimension': 'COLUMNS',
                                'startIndex': 2,  # column C
                                'endIndex': 3
                            }
                        }
                    }
                ]

                # Execute all updates in one API call
                sheet.batch_update({'requests': batch_updates})

                # Update the date in the new column
                tempSheet.update_cell(1, 3, today)
                print(f"Successfully updated sheet: {sheet_name}")
                return (sheet_name, True)
            except Exception as e:
                print(f"Error updating sheet {sheet_name}: {str(e)}")
                return (sheet_name, False)

        failed_sheets = []
        # Use ThreadPoolExecutor to process sheets in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks and store future objects
            future_to_sheet = {executor.submit(
                update_single_sheet, sheet_name): sheet_name for sheet_name in sheets}

            # Process completed tasks as they finish
            # Set timeout to 25 seconds to allow for response time
            for future in as_completed(future_to_sheet, timeout=25):
                sheet_name = future_to_sheet[future]
                try:
                    _, success = future.result()
                    if not success:
                        failed_sheets.append(sheet_name)
                except Exception as e:
                    print(
                        f"Sheet {sheet_name} generated an exception: {str(e)}")
                    failed_sheets.append(sheet_name)

        if failed_sheets:
            print(
                f"Failed to update following sheets: {', '.join(failed_sheets)}")
            return jsonify({"status": 400, "message": f"Some sheets failed to update: {', '.join(failed_sheets)}"})

        return jsonify({"status": 200, "message": 'All sheets updated successfully'})

    except Exception as e:
        print(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        return jsonify({"status": 400, "message": "Failed to update sheets"})
