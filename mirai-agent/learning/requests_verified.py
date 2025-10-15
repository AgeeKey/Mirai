"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 1/1
Learned: 2025-10-15T09:17:44.830107

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from a given URL using GET request.

    Args:
        url (str): The URL to send the request to.
        params (Optional[Dict[str, Any]]): Optional dictionary of query parameters to include in the request.

    Returns:
        Optional[Dict[str, Any]]: The JSON response as a dictionary if successful, None otherwise.
    """
    try:
        # Send a GET request to the provided URL with optional parameters
        response = requests.get(url, params=params)
        
        # Raise an HTTPError for bad responses (4xx and 5xx)
        response.raise_for_status()

        # Return the JSON response as a dictionary
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log request errors
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Log JSON decoding errors

    return None  # Return None if an error occurred

# Example usage
if __name__ == "__main__":
    api_url = "https://api.example.com/data"
    response_data = fetch_data(api_url, params={"key": "value"})
    
    if response_data is not None:
        print("Data fetched successfully:", response_data)
    else:
        print("Failed to fetch data.")