import gspread
from google.oauth2.service_account import Credentials
import http.client
import json

# Define column headers
COLUMNS = [
    "First Name",
    "Last Name",
    "Title",
    "Company",
    "Company Name for Emails",
    "Email"
]

# Google service account credentials and setup
service_account_info = {...}  # Assume credentials details are here

def setup_google_sheets(sheet_name):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
    client = gspread.authorize(credentials)
    return client.open(sheet_name)

def get_keywords(sheet):
    try:
        keywords_tab = sheet.worksheet("Keywords")
        return [keyword.strip() for keyword in keywords_tab.col_values(1)[1:] if keyword.strip()]
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError("The 'Keywords' tab does not exist in the sheet.")

def create_tab(sheet, keyword):
    try:
        sheet.add_worksheet(title=keyword, rows="100", cols="6")
    except Exception as e:
        print(f"Tab for {keyword} already exists or another error occurred: {e}")

def write_data_to_tab(sheet, keyword, data):
    try:
        worksheet = sheet.worksheet(keyword)
        worksheet.append_rows(data, value_input_option='USER_ENTERED')
    except Exception as e:
        print(f"Failed to write data to the tab {keyword}: {e}")

def fetch_people_by_company(api_endpoint, company_name, per_page=5):
    api_key = "your_api_key"
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'x-api-key': api_key,
    }
    payload = json.dumps({
        "person_titles": ["CEO", "Founder", "Owner", "President", "Chief Marketing Director", "Chief Marketing Officer", "Chief Executive Director"],
        "person_locations": ["United States"],
        "q_keywords": company_name,
        "company_revenue_min": 1000000,
        "per_page": per_page
    })
    conn = http.client.HTTPSConnection("api.apollo.io")
    try:
        conn.request("POST", api_endpoint, payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        return [[person['name'], person['title'], person.get('organization', {}).get('name', 'Unknown Company'), person.get('email', 'No Email')] for person in data.get('people', [])]
    except Exception as e:
        print(f"Error fetching data from Apollo for {company_name}: {e}")
        return []
    finally:
        conn.close()

def process_companies(sheet, api_endpoint):
    try:
        companies_worksheet = sheet.worksheet("Companies")
        company_names = companies_worksheet.col_values(1)[1:]  # Assuming company names are in the first column
        for company_name in company_names:
            if company_name:
                people_data = fetch_people_by_company(api_endpoint, company_name)
                write_data_to_tab(sheet, "Results", people_data)
    except Exception as e:
        print(f"Error processing companies: {e}")

def main():
    sheet_name = "ApolloAPIAutomation"
    api_endpoint = "/api/v1/mixed_people/search"
    sheet = setup_google_sheets(sheet_name)

    # Process keywords
    keywords = get_keywords(sheet)
    for keyword in keywords:
        create_tab(sheet, keyword)
        data = fetch_people_by_company(api_endpoint, keyword)  # Example function to fetch data
        write_data_to_tab(sheet, keyword, data)

    # Process companies after handling keywords
    process_companies(sheet, api_endpoint)

if __name__ == "__main__":
    main()
