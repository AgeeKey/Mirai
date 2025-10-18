"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 1/1
Learned: 2025-10-18T00:48:51.324020

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from the given URL with optional query parameters.

    Args:
        url (str): The URL to send the request to.
        params (Optional[Dict[str, Any]]): Optional query parameters for the request.

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the server, or None if an error occurs.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        return response.json()  # Return the JSON response

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")  # Print any other request-related error
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Print error if JSON decoding fails

    return None  # Return None if any error occurs

# Example usage
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 1}
    data = fetch_data(url, params)
    if data:
        print(data)  # Print the fetched data