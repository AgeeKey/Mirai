"""
json - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 1/1
Learned: 2025-10-13T17:24:10.677773

This code has been verified by MIRAI's NASA-level learning system.
"""

import json
from typing import Any, Dict

def read_json(file_path: str) -> Dict[str, Any]:
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Dict[str, Any]: The contents of the JSON file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load JSON data from the file
            return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        raise

def write_json(file_path: str, data: Dict[str, Any]) -> None:
    """
    Writes a dictionary to a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        data (Dict[str, Any]): The data to write to the JSON file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)  # Write JSON data to the file with indentation
    except IOError as e:
        print(f"Error writing to file: {e}")
        raise

# Example usage
if __name__ == "__main__":
    # Define the path to the JSON file
    json_file_path = 'example.json'
    
    # Example data to write to JSON
    example_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }
    
    # Write data to JSON file
    write_json(json_file_path, example_data)
    
    # Read data back from JSON file
    try:
        data = read_json(json_file_path)
        print(data)  # Output the read data
    except Exception as e:
        print(f"An error occurred: {e}")