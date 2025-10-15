"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 1/1
Learned: 2025-10-15T08:45:37.752746

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> dict:
    """
    Fetch data from a given URL using a GET request.

    Args:
        url (str): The URL to make the request to.
        params (Optional[dict]): A dictionary of query parameters to send with the request.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response content is not JSON.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For any request-related errors.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()  # Return the JSON content of the response
    except ValueError as e:
        raise ValueError("Response content is not in JSON format") from e
    except HTTPError as e:
        raise HTTPError(f"HTTP error occurred: {e}") from e
    except RequestException as e:
        raise RequestException(f"An error occurred while requesting data: {e}") from e

# Example usage
if __name__ == "__main__":
    url = "https://api.example.com/data"
    params = {"key": "value"}
    
    try:
        data = fetch_data(url, params)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f"Error occurred: {e}")