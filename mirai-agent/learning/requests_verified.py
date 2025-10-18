"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 1/1
Learned: 2025-10-18T17:02:32.927776

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from the specified URL with optional parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[Dict[str, Any]]): Optional query parameters for the request.

    Returns:
        Optional[Dict[str, Any]]: The JSON response data if successful, None otherwise.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return JSON response as a dictionary
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP error
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log request error
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Log JSON decoding error
    return None  # Return None if an error occurred

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://api.example.com/data"
    params = {"key": "value"}
    data = fetch_data(url, params)

    if data is not None:
        print("Data fetched successfully:", data)
    else:
        print("Failed to fetch data.")