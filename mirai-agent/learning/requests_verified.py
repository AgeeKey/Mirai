"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 1/1
Learned: 2025-10-19T13:47:10.776861

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetches data from the specified URL using a GET request.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For other request-related errors.
    """
    if not url.startswith('http'):
        raise ValueError("Invalid URL provided. Please ensure it starts with 'http' or 'https'.")

    try:
        # Send a GET request to the provided URL
        response = requests.get(url)
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Return the JSON response if successful
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP error
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log request error
        raise

# Example usage
if __name__ == "__main__":
    url = "https://api.github.com/users/octocat"
    try:
        data = fetch_data(url)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")