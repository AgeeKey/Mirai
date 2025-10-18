"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 1/1
Learned: 2025-10-18T06:20:43.646036

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException

def fetch_data(url: str) -> dict:
    """
    Fetch data from a given URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not in JSON format.
        RequestException: If an error occurs while making the request.
    """
    try:
        response = requests.get(url)  # Send the GET request
        response.raise_for_status()    # Raise an error for bad responses (4xx and 5xx)
        
        return response.json()         # Return the JSON content of the response

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        raise RequestException("HTTP request failed") from http_err
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")  # Handle JSON decoding errors
        raise ValueError("Response content is not valid JSON") from json_err
    except RequestException as req_err:
        print(f"Request exception: {req_err}")  # Handle other request-related errors
        raise

# Example usage
if __name__ == "__main__":
    url = "https://api.github.com/repos/psf/requests"  # Example URL
    try:
        data = fetch_data(url)  # Fetch data from the URL
        print(data)             # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exception that occurs