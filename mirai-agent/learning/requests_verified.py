"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.95
Tests Passed: 1/1
Learned: 2025-10-19T11:25:09.501017

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException

def fetch_data(url: str) -> dict:
    """
    Fetches data from the specified URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response content is not valid JSON.
        RequestException: If an error occurs during the request.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        # Raise an error for bad responses (4xx and 5xx status codes)
        response.raise_for_status()
        # Parse the response as JSON and return it
        return response.json()
    except ValueError as e:
        raise ValueError("Response content is not valid JSON") from e
    except RequestException as e:
        raise RequestException(f"An error occurred while fetching data: {e}")

if __name__ == "__main__":
    # Example URL to fetch data from
    url = "https://jsonplaceholder.typicode.com/posts/1"
    
    try:
        # Fetch data and print the result
        data = fetch_data(url)
        print(data)
    except (ValueError, RequestException) as e:
        print(e)