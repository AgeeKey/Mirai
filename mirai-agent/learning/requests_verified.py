"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 1/1
Learned: 2025-10-22T07:49:58.323515

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException

def fetch_data(url: str) -> dict:
    """
    Fetch data from a given URL using a GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For other request-related errors.
    """
    if not url.startswith('http'):
        raise ValueError("Invalid URL provided. URL must start with 'http' or 'https'.")

    try:
        # Sending a GET request to the specified URL
        response = requests.get(url)
        
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()

        # Return the JSON content of the response
        return response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        raise

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://jsonplaceholder.typicode.com/todos/1"
    try:
        data = fetch_data(url)
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")