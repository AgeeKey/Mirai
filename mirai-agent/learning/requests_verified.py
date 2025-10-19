"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 1/1
Learned: 2025-10-19T21:40:35.361632

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict

def fetch_data(url: str, params: Optional[Dict[str, str]] = None) -> Optional[Dict]:
    """
    Fetches data from a given URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[Dict[str, str]]): Optional query parameters to include in the request.

    Returns:
        Optional[Dict]: The JSON response data if successful, None otherwise.
    """
    try:
        # Send a GET request to the specified URL with optional parameters
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP error responses
        response.raise_for_status()
        
        # Return the JSON response content
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
    
    return None

if __name__ == "__main__":
    # Example usage of the fetch_data function
    api_url = "https://api.example.com/data"
    query_params = {"key": "value"}
    
    data = fetch_data(api_url, params=query_params)
    
    if data is not None:
        print("Fetched data:", data)
    else:
        print("Failed to fetch data.")