"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-14T19:21:45.733557

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException

def fetch_data(url: str) -> dict:
    """Fetch data from the given URL and return it as a dictionary.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response cannot be converted to JSON.
        RequestException: For other request-related errors.
    """
    try:
        response = requests.get(url)  # Make a GET request to the URL
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return the response as JSON

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        raise
    except ValueError as json_err:
        print(f"Error parsing JSON response: {json_err}")  # Handle JSON parsing errors
        raise ValueError("Invalid JSON response") from json_err
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Handle any other request-related errors
        raise

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid URL
    try:
        data = fetch_data(url)  # Fetch data from the URL
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any unhandled exceptions