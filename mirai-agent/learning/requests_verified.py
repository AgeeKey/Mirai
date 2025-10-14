"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 1/1
Learned: 2025-10-14T10:51:13.680066

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> dict:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[dict]): A dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For any other requests-related issues.
    """
    if not url:
        raise ValueError("The URL must not be empty.")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP error
        raise
    except RequestException as req_err:
        print(f"Error occurred during the request: {req_err}")  # Log other request errors
        raise

# Example usage:
if __name__ == "__main__":
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        params = {"userId": 1}
        data = fetch_data(url, params)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Log any errors during the fetch