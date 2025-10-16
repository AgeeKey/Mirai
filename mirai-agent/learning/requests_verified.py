"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-16T16:12:37.192625

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException

def fetch_data(url: str) -> dict:
    """
    Fetch data from the given URL and return it as a dictionary.

    :param url: The URL to fetch data from.
    :return: A dictionary containing the JSON response.
    :raises ValueError: If the response is not JSON.
    :raises RequestException: For general request-related errors.
    """
    try:
        response = requests.get(url)  # Send a GET request to the URL
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response as a dictionary
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Log JSON decoding errors
        raise ValueError("Response content is not valid JSON.")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log other request-related errors
        raise

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid URL
    try:
        data = fetch_data(url)  # Fetch data from the URL
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions raised