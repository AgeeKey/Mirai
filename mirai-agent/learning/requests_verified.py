"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 1/1
Learned: 2025-10-22T00:05:44.420417

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from a given URL using an HTTP GET request.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        Dict[str, Any]: The JSON response data if the request is successful.

    Raises:
        ValueError: If the response is not valid JSON.
        RequestException: For general request-related errors.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        # Raise an HTTPError for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Attempt to return the response as JSON
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log the HTTP error
        raise
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")  # Log the JSON error
        raise ValueError("Response content is not valid JSON.")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log the request error
        raise

if __name__ == "__main__":
    # Example URL to fetch data from
    example_url = "https://jsonplaceholder.typicode.com/todos/1"
    
    try:
        # Fetch data from the example URL
        data = fetch_data(example_url)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Log any other errors