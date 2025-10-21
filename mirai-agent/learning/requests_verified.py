"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-21T11:21:51.824507

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> Optional[dict]:
    """
    Fetch data from the specified URL with optional query parameters.

    Args:
        url (str): The URL to fetch data from.
        params (Optional[dict]): A dictionary of query parameters to include in the request.

    Returns:
        Optional[dict]: The JSON response from the server if the request is successful, None otherwise.
    """
    try:
        # Send a GET request to the specified URL with optional parameters
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")  # Print any other request-related errors
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Print errors related to JSON decoding
    
    return None  # Return None if the request failed

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://api.example.com/data"
    query_params = {"key": "value"}
    
    data = fetch_data(url, params=query_params)
    if data is not None:
        print(data)  # Print the fetched data