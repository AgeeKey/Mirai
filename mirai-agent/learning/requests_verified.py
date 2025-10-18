"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 1/1
Learned: 2025-10-18T07:08:05.897414

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException

def fetch_data(url: str) -> dict:
    """
    Fetch data from a given URL using an HTTP GET request.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        dict: The JSON response from the server if the request is successful.

    Raises:
        ValueError: If the response content is not JSON.
        RequestException: If the request fails for any reason.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Attempt to return the response as JSON
        return response.json()
    except ValueError:
        raise ValueError("Response content is not in JSON format.")
    except RequestException as e:
        raise RequestException(f"An error occurred: {e}")

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid URL
    try:
        data = fetch_data(url)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"Error fetching data: {e}")