"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-20T03:10:47.775718

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException

def fetch_data(url: str) -> dict:
    """
    Fetch data from the specified URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response data.

    Raises:
        ValueError: If the response is not JSON or the status code is not 200.
        RequestException: If there is a problem with the request.
    """
    try:
        response = requests.get(url)  # Make a GET request to the URL
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON content of the response
    except ValueError as e:
        raise ValueError("Response is not valid JSON") from e
    except RequestException as e:
        raise RequestException(f"Error fetching data: {e}") from e

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid API endpoint
    try:
        data = fetch_data(url)  # Fetch data from the given URL
        print(data)  # Print the fetched data
    except Exception as e:
        print(e)  # Print any errors that occur