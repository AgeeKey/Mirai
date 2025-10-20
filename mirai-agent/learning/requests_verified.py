"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.95
Tests Passed: 1/1
Learned: 2025-10-20T12:25:09.980546

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict

def fetch_data(url: str, params: Optional[Dict[str, str]] = None) -> Optional[dict]:
    """
    Fetch data from a given URL with optional query parameters.
    
    Args:
        url (str): The URL to send the GET request to.
        params (Optional[Dict[str, str]]): Optional dictionary of query parameters.
        
    Returns:
        Optional[dict]: The JSON response as a dictionary if successful, None otherwise.
    """
    try:
        # Send a GET request to the specified URL with optional parameters
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP error responses
        response.raise_for_status()
        
        # Return the JSON response as a dictionary
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print HTTP error message
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Print general request error message
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")  # Print JSON decoding error message
    
    return None  # Return None if an error occurred

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://api.example.com/data"
    query_params = {"key": "value"}
    
    # Fetch the data and print the result
    result = fetch_data(url, query_params)
    print(result)