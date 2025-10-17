"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 1/1
Learned: 2025-10-17T15:07:10.541889

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def get_data_from_api(url: str) -> Dict[str, Any]:
    """
    Fetch data from a specified API endpoint.

    Args:
        url (str): The URL of the API endpoint.

    Returns:
        Dict[str, Any]: The JSON response from the API.

    Raises:
        ValueError: If the response is not JSON or the request fails.
    """
    try:
        response = requests.get(url)
        # Raise an error for bad responses (4XX and 5XX)
        response.raise_for_status()  
        
        # Attempt to parse JSON response
        return response.json()  
    except HTTPError as http_err:
        raise ValueError(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except RequestException as req_err:
        raise ValueError(f"Request error occurred: {req_err}")  # Handle other request issues
    except ValueError as json_err:
        raise ValueError(f"Invalid JSON response: {json_err}")  # Handle JSON parsing errors

if __name__ == "__main__":
    api_url = "https://api.example.com/data"  # Replace with a real API URL
    try:
        data = get_data_from_api(api_url)
        print(data)  # Output the fetched data
    except ValueError as e:
        print(e)  # Print any error messages