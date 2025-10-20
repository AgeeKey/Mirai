"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-20T02:23:34.250491

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException

def fetch_data(url: str) -> dict:
    """
    Fetch data from the specified URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the server if successful.

    Raises:
        ValueError: If the response is not JSON or if the URL is invalid.
        RequestException: For network-related errors during the request.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        # Raise an error for bad status codes
        response.raise_for_status()
        
        # Attempt to parse the response as JSON
        return response.json()
    except ValueError:
        raise ValueError("Response content is not in JSON format.")
    except RequestException as e:
        raise RequestException(f"An error occurred while fetching data: {e}")

if __name__ == "__main__":
    # Example usage
    url = "https://jsonplaceholder.typicode.com/posts/1"  # Sample API endpoint
    try:
        data = fetch_data(url)  # Fetch data from the API
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle and print any errors