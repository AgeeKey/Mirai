"""
os - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-13T23:52:25.970187

This code has been verified by MIRAI's NASA-level learning system.
"""

import os
from typing import List, Optional

def list_files_in_directory(directory: str) -> Optional[List[str]]:
    """
    List all files in the specified directory.

    Args:
        directory (str): The path to the directory to list files from.

    Returns:
        Optional[List[str]]: A list of filenames in the directory, or None if an error occurs.
    """
    try:
        # Check if the provided path is a directory
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory.")
            return None
        
        # List all files in the directory
        files = os.listdir(directory)
        return [file for file in files if os.path.isfile(os.path.join(directory, file))]
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main() -> None:
    """
    Main function to execute the file listing.
    """
    directory_path = input("Enter the directory path to list files: ")
    files = list_files_in_directory(directory_path)
    
    if files is not None:
        print("Files in directory:")
        for file in files:
            print(file)

if __name__ == "__main__":
    main()