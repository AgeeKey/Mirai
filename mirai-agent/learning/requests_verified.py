"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 1/1
Learned: 2025-10-19T01:56:58.428269

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def fetch_data(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetch data from a specified URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Dict[str, Any], optional): A dictionary of query parameters to include in the request.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the response does not contain valid JSON.
        HTTPError: If an HTTP error occurs during the request.
        RequestException: For any other request-related errors.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        return response.json()  # Parse and return the JSON response

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except ValueError as json_err:
        print(f"Failed to parse JSON: {json_err}")
        raise
    except RequestException as req_err:
        print(f"Error during requests to {url}: {req_err}")
        raise

# Example usage
if __name__ == "__main__":
    url = "https://api.example.com/data"
    query_params = {"key": "value"}

    try:
        data = fetch_data(url, params=query_params)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")