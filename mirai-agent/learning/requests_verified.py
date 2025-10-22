"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 1/1
Learned: 2025-10-22T14:49:33.205916

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any

def fetch_data(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetch data from the given URL using a GET request.

    Args:
        url (str): The URL to send the request to.
        params (Dict[str, Any], optional): Optional query parameters for the request.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the response is not in JSON format.
        HTTPError: If an HTTP error occurs during the request.
        RequestException: For other request-related errors.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        return response.json()  # Return the JSON response

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        raise
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Handle JSON decoding errors
        raise ValueError("Response content is not valid JSON.")
    except RequestException as req_err:
        print(f"Request error: {req_err}")  # Handle other request errors
        raise

# Example usage:
if __name__ == "__main__":
    url = "https://api.example.com/data"
    query_params = {'key': 'value'}
    
    try:
        data = fetch_data(url, query_params)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any errors that occur during the fetch