"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-17T09:42:49.442376

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException

def fetch_data(url: str) -> dict:
    """
    Fetch data from the specified URL and return it as a dictionary.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response does not contain valid JSON.
        RequestException: If there is an error during the request.
    """
    try:
        response = requests.get(url)  # Send a GET request to the URL
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        return response.json()  # Return the response as a JSON dictionary

    except ValueError as ve:
        raise ValueError("Response content is not valid JSON.") from ve
    except RequestException as req_err:
        raise RequestException(f"An error occurred while fetching data: {req_err}") from req_err

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid API endpoint
    try:
        data = fetch_data(url)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions that arise