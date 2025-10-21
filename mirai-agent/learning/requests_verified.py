"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 1/1
Learned: 2025-10-21T18:40:50.981685

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException
from typing import Dict, Any

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from the given URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the response is not valid JSON.
        RequestException: If there is an error during the request.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Attempt to parse the response as JSON
    except ValueError as e:
        raise ValueError("Response content is not valid JSON") from e
    except RequestException as e:
        raise RequestException(f"An error occurred while fetching data: {e}")

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid API endpoint
    try:
        data = fetch_data(url)
        print("Fetched data:", data)
    except Exception as e:
        print("Error:", e)