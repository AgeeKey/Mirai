"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-17T11:19:07.140296

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from a given URL using GET request.

    :param url: The URL to fetch data from.
    :param params: Optional dictionary of query parameters to include in the request.
    :return: Parsed JSON response as a dictionary or None if an error occurs.
    """
    try:
        # Make the GET request
        response = requests.get(url, params=params)
        
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Attempt to parse the JSON response
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print HTTP error
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Print request error
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Print JSON parsing error
    
    return None  # Return None if any error occurs

# Example usage
if __name__ == "__main__":
    url = "https://api.example.com/data"
    parameters = {"key": "value"}
    
    result = fetch_data(url, parameters)
    if result:
        print("Fetched data:", result)
    else:
        print("Failed to fetch data.")