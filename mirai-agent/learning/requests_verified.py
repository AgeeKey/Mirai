"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 1/1
Learned: 2025-10-17T11:03:06.310781

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict

def fetch_data(url: str, params: Optional[Dict[str, str]] = None) -> Optional[Dict]:
    """
    Fetch data from a given URL using a GET request.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[Dict[str, str]]): Optional query parameters to include in the request.

    Returns:
        Optional[Dict]: The JSON response data if the request is successful, None otherwise.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Return the response as a JSON dictionary
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")  # Handle other request errors
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Handle JSON decoding errors
    return None  # Return None if an error occurred

if __name__ == "__main__":
    # Example usage
    url = "https://api.example.com/data"
    params = {"key": "value"}
    data = fetch_data(url, params)

    if data is not None:
        print(data)  # Output the fetched data
    else:
        print("Failed to fetch data.")