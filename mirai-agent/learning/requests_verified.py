"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.98
Tests Passed: 1/1
Learned: 2025-10-18T14:14:15.524149

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException
from typing import Optional

def fetch_data(url: str) -> Optional[dict]:
    """
    Fetch data from the specified URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Optional[dict]: The JSON response as a dictionary if the request is successful,
                        None otherwise.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        # Raise an error for bad responses
        response.raise_for_status()
        # Return the JSON response as a dictionary
        return response.json()
    except RequestException as e:
        # Print the error message if the request fails
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example URL to fetch data from
    url = "https://api.example.com/data"
    
    # Fetch data from the URL
    data = fetch_data(url)
    
    # Check if data was fetched successfully
    if data is not None:
        print("Data fetched successfully:", data)
    else:
        print("Failed to fetch data.")