"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 1/1
Learned: 2025-10-21T08:25:02.527966

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException

def fetch_data(url: str) -> dict:
    """
    Fetches JSON data from a given URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response parsed into a dictionary.

    Raises:
        ValueError: If the response is not JSON.
        RequestException: For other request-related errors.
    """
    try:
        response = requests.get(url)  # Send a GET request to the URL
        response.raise_for_status()  # Raise an error for HTTP error responses
        return response.json()  # Parse and return the JSON response
    except ValueError:
        raise ValueError("Response content is not valid JSON.")  # Handle non-JSON responses
    except RequestException as e:
        raise RequestException(f"An error occurred: {e}")  # Handle request errors

if __name__ == "__main__":
    # Example URL to fetch data from
    example_url = "https://jsonplaceholder.typicode.com/posts/1"
    try:
        data = fetch_data(example_url)  # Call the fetch_data function
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"Error: {e}")  # Print any errors that occur