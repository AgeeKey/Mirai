"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 1/1
Learned: 2025-10-20T13:30:10.504833

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> Optional[dict]:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[dict]): A dictionary of query parameters to include in the request.

    Returns:
        Optional[dict]: The JSON response data if the request is successful, None otherwise.
    """
    try:
        # Send GET request
        response = requests.get(url, params=params)
        
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Parse and return the JSON response
        return response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP error
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log request error
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Log JSON decoding error
    return None

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid URL
    params = {"key": "value"}  # Replace with valid parameters if needed
    
    data = fetch_data(url, params)
    if data is not None:
        print("Data retrieved successfully:", data)
    else:
        print("Failed to retrieve data.")