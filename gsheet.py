import gspread
from google.oauth2.service_account import Credentials

# Define columns for the Google Sheet
COLUMNS = [
    "First Name", "Last Name", "Title", "Company", "Email"
]

# Embedded credentials (for testing purposes only)
credentials = {
   
  }

def setup_google_sheets(sheet_name):
    """
    Sets up the Google Sheets client using credentials and opens the specified sheet.

    Args:
        sheet_name (str): The name of the Google Sheet to open.

    Returns:
        gspread.Spreadsheet: The Google Sheets object.
    """
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_info(credentials, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

def populate_data(sheet, tab_name, data):
    """
    Append formatted data into a specified Google Sheets tab.

    Args:
        sheet (gspread.Spreadsheet): The Google Sheets object.
        tab_name (str): Name of the tab to populate.
        data (list): List of rows to populate in the tab.
    """
    try:
        # Access or create the worksheet
        try:
            worksheet = sheet.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=tab_name, rows=100, cols=len(COLUMNS))
            worksheet.append_row(COLUMNS)  # Set headers

        # Debugging: Print rows to confirm they are populated correctly
        print(f"Rows to append: {data}")

        # Append rows
        if data:
            worksheet.append_rows(data)
            print(f"Successfully appended data to tab: {tab_name}")
        else:
            print(f"No valid rows to append for tab: {tab_name}")
    except Exception as e:
        print(f"Error in populate_data: {e}")
