"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.96
Tests Passed: 1/1
Learned: 2025-10-19T17:59:40.788842

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException

def fetch_data(url: str) -> dict:
    """
    Fetch data from a given URL using a GET request.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not JSON.
        RequestException: If there is an error during the request.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        # Raise an error for bad responses
        response.raise_for_status()
        
        # Attempt to parse the response as JSON
        return response.json()

    except RequestException as e:
        # Handle any request-related errors
        print(f"Request failed: {e}")
        raise  # Re-raise the exception for further handling

    except ValueError:
        # Handle JSON decoding errors
        print("Response content is not in JSON format.")
        raise

if __name__ == "__main__":
    # Example URL to fetch data from
    example_url = "https://api.github.com/repos/psf/requests"
    try:
        data = fetch_data(example_url)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")