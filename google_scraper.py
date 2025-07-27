import http.client
import json

def fetch_people_data(api_endpoint, keyword, per_page=5):
    """
    Fetch people data from Apollo API based on the given keyword.

    Args:
        api_endpoint (str): Apollo API endpoint.
        keyword (str): Keyword to search for.
        per_page (int): Number of results per page.

    Returns:
        list: Sorted list of people with their details, including emails where available.
    """
    api_key = ""

    if not api_key:
        raise ValueError("API key not found. Ensure it's set in the .env file.")

    # JSON Payload for the API Request
    payload = json.dumps({
    })

    # Headers for the API Request
    headers = {
        
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

            # Format results to include emails
            formatted_results = [
                {
                    "name": person['name'],
                    "title": person['title'],
                    "organization": person.get('organization', {}).get('name', 'Unknown Company'),
                    "email": person.get('email', 'No Email')  # Include email if available, otherwise 'No Email'
                }
                for person in sorted_people
            ]
            return formatted_results
        else:
            print(f"No results found for keyword: {keyword}")
            return []

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

    finally:
        conn.close()


def fetch_dummy_people_data():
    """
    Returns dummy data for testing without making actual API requests.

    Returns:
        list: A list of dictionaries, each representing a person's details.
    """
    # Example dummy data
    dummy_data = [
        {"name": "John Doe", "title": "CEO", "organization": "Tech Innovations"},
        {"name": "Jane Smith", "title": "CMO", "organization": "Health Solutions"},
        {"name": "Alice Johnson", "title": "Founder", "organization": "Eco Foods"},
        {"name": "Bob Brown", "title": "President", "organization": "Auto Advancements"},
        {"name": "Carol White", "title": "Chief Executive Officer", "organization": "Future Tech"}
    ]

    return dummy_data


# Example usage
if __name__ == "__main__":
    API_ENDPOINT = ""
    
    keyword = ""

    results = fetch_people_data(API_ENDPOINT, keyword)
    for result in results:
        print(f"{result['name']} - {result['title']} at {result['organization']} with email: {result['email']}")
