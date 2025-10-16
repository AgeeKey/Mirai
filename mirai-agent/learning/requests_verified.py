"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 1/1
Learned: 2025-10-16T18:55:21.074888

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from the specified URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For other request-related errors.
    """
    if not url.startswith("http"):
        raise ValueError("Invalid URL. It must start with http or https.")

    try:
        # Sending a GET request to the specified URL
        response = requests.get(url)
        
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Return the JSON response if successful
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except RequestException as req_err:
        print(f"Error during requests to {url}: {req_err}")
        raise

if __name__ == "__main__":
    # Example URL to fetch data from
    example_url = "https://jsonplaceholder.typicode.com/posts/1"
    
    try:
        data = fetch_data(example_url)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")