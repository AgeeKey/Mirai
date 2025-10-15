"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-15T20:08:32.576420

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to fetch data from.
        params (Optional[Dict[str, Any]]): A dictionary of query parameters.

    Returns:
        Optional[Dict[str, Any]]: The JSON response as a dictionary, or None if an error occurs.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()  # Return the response as a JSON dictionary
    except RequestException as e:
        print(f"Error occurred while fetching data: {e}")
        return None

if __name__ == "__main__":
    url = "https://api.example.com/data"
    parameters = {"key": "value"}
    
    result = fetch_data(url, params=parameters)
    
    if result is not None:
        print("Data fetched successfully:", result)
    else:
        print("Failed to fetch data.")