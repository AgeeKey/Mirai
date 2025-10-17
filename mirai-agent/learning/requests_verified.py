"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-17T22:08:56.263139

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
        ValueError: If the response is not JSON.
        RequestException: If an error occurs during the request.
    """
    try:
        response = requests.get(url)  # Send a GET request to the URL
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        return response.json()  # Return the response JSON data

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except ValueError as json_err:
        print(f"Error parsing JSON: {json_err}")  # Log JSON parsing errors
        raise ValueError("Response content is not valid JSON.")
    except RequestException as req_err:
        print(f"Error during requests to {url}: {req_err}")  # Log other request errors
        raise

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Example URL
    try:
        data = fetch_data(url)  # Fetch data from the URL
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions