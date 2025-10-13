"""
JSON - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 1/1
Learned: 2025-10-13T13:02:36.175368

This code has been verified by MIRAI's NASA-level learning system.
"""

import json
from typing import Any, Dict


def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Reads a JSON file and returns its content as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Dict[str, Any]: The content of the JSON file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)  # Load JSON content into a dictionary
    except FileNotFoundError as e:
        print(f"Error: {e}")  # File not found error handling
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")  # JSON decoding error handling
        raise


def write_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """
    Writes a dictionary to a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        data (Dict[str, Any]): The dictionary to write to the JSON file.

    Raises:
        IOError: If the file cannot be written.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)  # Write data as JSON with indentation
    except IOError as e:
        print(f"Error writing to file: {e}")  # File writing error handling
        raise


if __name__ == "__main__":
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "is_student": False
    }

    # Write sample data to a JSON file
    write_json_file('sample.json', sample_data)

    # Read the data back from the JSON file
    loaded_data = read_json_file('sample.json')
    print(loaded_data)  # Output the loaded JSON data