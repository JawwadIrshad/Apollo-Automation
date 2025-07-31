# from dotenv import load_dotenv

from src.google_sheets import setup_google_sheets, get_keywords, create_tab, write_data_to_tab
from src.google_scraper import fetch_people_data, fetch_dummy_people_data
from src.gsheet import setup_google_sheets, populate_data
from src.apollo import mock_fetch_people_by_company, fetch_people_by_company


# Constants defining the sheet name and the API endpoint for fetching data
SHEET_NAME = "" #put sheet name here
API_ENDPOINT = ""

def main():
    user_input = input("Enter 'Y' to run Apollo companies people search automation or 'N' to exit: ").strip().lower()
    if user_input != 'y':
        print("Exiting...")
        return

    try:
        # Attempt to initialize Google Sheets connection
        sheet = setup_google_sheets(SHEET_NAME)
        print("Google Sheets successfully initialized!")  # Success prompt
    except Exception as e:
        print("Failed to initialize Google Sheets connection:", e)
        return

    try:
        keywords = get_keywords(sheet)
        if not keywords:
            print("No keywords found, exiting.")
            return
    except ValueError as e:
        print("Error retrieving keywords:", e)
        return

    for keyword in keywords:
        print(f"Processing keyword: {keyword}")
        try:
            create_tab(sheet, keyword)
            data = fetch_people_data(API_ENDPOINT, keyword)
            # data = fetch_dummy_people_data()
        except Exception as e:
            print(f"Error fetching data for keyword '{keyword}':", e)
            continue

        try:
            formatted_data = [
                [
                    person.get('name', '').split()[0],  # First Name
                    ' '.join(person.get('name', '').split()[1:]),  # Last Name
                    person.get('title', ''),  # Title
                    person.get('organization', 'Unknown Company'),  # Company
                    person.get('organization', 'Unknown Company'),  # Company Name for Emails
                    person.get('email', 'No Email'),  # Email
                    'Verified'  # Email Status
                ]
                for person in data
            ]
            write_data_to_tab(sheet, keyword, formatted_data)
            print(f"Successfully wrote data to tab for keyword '{keyword}'.")
        except Exception as e:
            print(f"Error formatting or writing data for keyword '{keyword}':", e)

    # Load environment variables
    # load_dotenv()

    # Constants
    SHEET_NAME = ""
    API_ENDPOINT = ""
    TAB_NAME = "Results"

    # Prompt for Google Sheets initialization
    try:
        print("Initializing Google Sheets...")
        sheet = setup_google_sheets(SHEET_NAME)
        print("Google Sheets successfully initialized!")
    except Exception as e:
        print(f"Failed to initialize Google Sheets: {e}")
        return

    # Prompt user to confirm running the automation
    user_input = input("Do you want to run the Apollo automation? (yes/no): ").strip().lower()
    if user_input not in ('yes', 'y'):
        print("Automation canceled.")
        return

    # Step 1: Get the 'Companies' tab
    try:
        companies_tab = sheet.worksheet("Companies")
        print("Accessed 'Companies' tab successfully.")
    except Exception as e:
        print(f"Error accessing 'Companies' tab: {e}")
        return

    # Step 2: Read company names from the 'Companies' column
    company_names = companies_tab.col_values(1)[1:]  # Skip the header row
    if not company_names:
        print("No company names found in the 'Companies' tab.")
        return

    # Step 3: Fetch and populate data for each company
    for company_name in company_names:
        if not company_name.strip():
            continue

        print(f"Processing company: {company_name}")

        # Fetch data from Apollo
        # data = mock_fetch_people_by_company(API_ENDPOINT, company_name)  # Mock function for testing
        data = fetch_people_by_company(API_ENDPOINT, company_name)  # Use this for real API calls
        print(f"Fetched data for {company_name}: {data}")

        if data:
            try:
                # Prepare formatted data for Google Sheets
                formatted_data = []
                for person in data:
                    if isinstance(person, dict):
                        name_parts = person.get("name", "").split(" ", 1)
                        first_name = name_parts[0] if name_parts else "Unknown"
                        last_name = name_parts[1] if len(name_parts) > 1 else "Unknown"

                        formatted_data.append([
                            first_name,
                            last_name,
                            person.get("title", "Unknown Title"),
                            person.get("organization", "Unknown Company"),
                            person.get("email", "No Email")
                        ])

                if formatted_data:
                    # Write formatted data to the Google Sheet
                    populate_data(sheet, TAB_NAME, formatted_data)
                    print(f"Data for '{company_name}' appended successfully.")
                else:
                    print(f"No valid data for '{company_name}'.")
            except Exception as e:
                print(f"Error populating data for '{company_name}': {e}")
        else:
            print(f"No data fetched for '{company_name}'.")



if __name__ == "__main__":
    main()
