"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 1/1
Learned: 2025-10-17T21:37:21.327652

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
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not JSON.
        RequestException: If there is a problem with the HTTP request.
    """
    try:
        response = requests.get(url)  # Send a GET request
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        # Attempt to parse the response as JSON
        return response.json()
    except ValueError as ve:
        raise ValueError("Response is not in JSON format.") from ve
    except RequestException as req_err:
        raise RequestException(f"HTTP request failed: {req_err}") from req_err

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid API endpoint
    try:
        data = fetch_data(url)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")