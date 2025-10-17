"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 1/1
Learned: 2025-10-17T00:53:40.589048

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from a given URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the response does not contain valid JSON.
        RequestException: For any request-related errors.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        
        # Raise an HTTPError for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Return the JSON content if the response is successful
        return response.json()
    
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Log HTTP error
        raise
    except ValueError as json_err:
        print(f'JSON decode error: {json_err}')  # Log JSON decode error
        raise ValueError("Response content is not valid JSON.")
    except RequestException as req_err:
        print(f'Error occurred during the request: {req_err}')  # Log request error
        raise

# Example usage
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts/1"  # Example URL
    try:
        data = fetch_data(url)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f'An error occurred: {e}')  # Log any other errors