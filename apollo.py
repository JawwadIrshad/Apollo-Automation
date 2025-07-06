import http.client
import json
import os
# from dotenv import load_dotenv
def fetch_people_by_company(api_endpoint, company_name, per_page=5):
    """
    Fetch people data from Apollo API based on the given company name.

    Args:
        api_endpoint (str): Apollo API endpoint.
        company_name (str): Name of the company to search for.
        per_page (int): Number of results per page.

    Returns:
        list: Sorted list of people with their details.
    """
    # Load environment variables
    # load_dotenv()
    api_key = ""

    # if not api_key:
    #     raise ValueError("API key not found. Ensure it's set in the .env file.")

    # JSON Payload for the API Request
    payload = json.dumps({
        "person_titles": [
            "CEO", "Founder", "Owner", "President",
            "Chief Marketing Director", "Chief Marketing Officer", "Chief Executive Director"
        ],
        "person_locations": ["United States"],
        "q_keywords": company_name,  # Use the company name as a keyword
        "company_revenue_min": 1000000,
        "per_page": per_page
    })

    # Headers for the API Request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'x-api-key': api_key,
    }

    # Establish HTTPS Connection
    conn = http.client.HTTPSConnection("api.apollo.io")

    try:
        # Make the POST Request
        conn.request("POST", api_endpoint, payload, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')

        # Parse the JSON Data
        data = json.loads(data)

        # Check if "people" key exists and has results
        if "people" in data and data["people"]:
            sorted_people = sorted(data['people'], key=lambda person: person['name'])

            # Format results
            formatted_results = [
                {
                    "name": person['name'],
                    "title": person['title'],
                    "organization": person.get('organization', {}).get('name', 'Unknown Company'),
                    "email": person.get('email')  # Include email irrespective of its status
                }
                for person in sorted_people
            ]
            return formatted_results
        else:
            print(f"No results found for company: {company_name}")
            return []

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

    finally:
        conn.close()


def mock_fetch_people_by_company(api_endpoint, company_name, per_page=5):
   
    print(f"Mock fetching data for company: {company_name}")
    # Simulate a list of people based on the company name and per_page limit
    simulated_people = [
        {
            "name": "John Doe",
            "title": "CEO",
            "organization": company_name,
            "email": "johndoe@example.com"
        },
        {
            "name": "Jane Smith",
            "title": "CFO",
            "organization": company_name,
            "email": "janesmith@example.com"
        },
        {
            "name": "Alex Johnson",
            "title": "CTO",
            "organization": company_name,
            "email": "alexjohnson@example.com"
        }
    ][:per_page]  # Limit the results based on per_page

    return simulated_people
