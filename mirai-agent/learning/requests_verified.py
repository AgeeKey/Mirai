"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 1/1
Learned: 2025-10-16T14:51:55.773607

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException

def fetch_data(url: str) -> dict:
    """
    Fetches data from the specified URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the server if the request is successful.

    Raises:
        ValueError: If the response is not JSON.
        RequestException: For any request-related errors.
    """
    try:
        response = requests.get(url)  # Send a GET request
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Attempt to parse the response as JSON
        return response.json()
    except ValueError as ve:
        raise ValueError("Response is not in JSON format") from ve
    except RequestException as e:
        raise RequestException(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://api.github.com/repos/psf/requests"  # URL to fetch data from
    try:
        data = fetch_data(url)
        print(data)  # Print the retrieved data
    except Exception as e:
        print(f"An error occurred: {e}")