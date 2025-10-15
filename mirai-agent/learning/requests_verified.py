"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 1/1
Learned: 2025-10-15T04:59:06.850675

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException

def fetch_data(url: str) -> dict:
    """Fetch data from the specified URL and return the response as a dictionary.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not in JSON format.
        HTTPError: If an HTTP error occurs during the request.
        RequestException: For any other request-related issues.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        
        # Raise an HTTPError for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Attempt to return the response as JSON
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except ValueError as json_err:
        print(f"Error decoding JSON: {json_err}")
        raise ValueError("Response not in JSON format") from json_err
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        raise

if __name__ == "__main__":
    # Example URL for fetching data
    url = "https://api.github.com/repos/psf/requests"
    
    try:
        data = fetch_data(url)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")