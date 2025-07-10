# backend_metadata_fetcher.py

import requests
from openpyxl import Workbook
from datetime import datetime
from io import BytesIO

def fetch_user_metadata_to_memory(user_ids):
    base_url = "https://sso-dev.tpml.in/auth/get-user-metadata?userId="

    wb = Workbook()
    ws = wb.active
    ws.title = "User Metadata"
    headers = ["User ID", "Display Name", "First Name", "Last Name", "Email", "Gender", "DOB", "College"]
    ws.append(headers)

    for user_id in user_ids:
        url = base_url + user_id
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                metadata = data.get("metadata", {})
                display_name = metadata.get("displayName", "N/A")
                first_name = metadata.get("first_name", "N/A")
                last_name = metadata.get("last_name", "N/A")
                email = metadata.get("dh", {}).get("newsLetter", {}).get("email", "N/A")
                gender = metadata.get("gender", "N/A")
                dob = f'{metadata.get("dob", {}).get("day", "N/A")}-{metadata.get("dob", {}).get("month", "N/A")}-{metadata.get("dob", {}).get("year", "N/A")}'
                college = metadata.get("college", "N/A")
                row = [user_id, display_name, first_name, last_name, email, gender, dob, college]
            else:
                row = [user_id, "Failed to retrieve data", "", "", "", "", "", ""]
        except Exception as e:
            row = [user_id, f"Error: {str(e)}", "", "", "", "", "", ""]
        ws.append(row)

    # Save to in-memory stream
    excel_stream = BytesIO()
    wb.save(excel_stream)
    excel_stream.seek(0)
    
    filename = f"user_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return excel_stream, filename
