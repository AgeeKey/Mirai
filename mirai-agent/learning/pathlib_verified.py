"""
pathlib - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 1/1
Learned: 2025-10-13T17:24:33.519144

This code has been verified by MIRAI's NASA-level learning system.
"""

from pathlib import Path
import os

def create_file_with_content(file_path: Path, content: str) -> None:
    """
    Creates a file with the specified content at the given path.

    Args:
        file_path (Path): The path where the file will be created.
        content (str): The content to write to the file.

    Raises:
        FileExistsError: If the file already exists.
        IOError: If there is an error writing to the file.
    """
    if file_path.exists():
        raise FileExistsError(f"The file {file_path} already exists.")
    
    try:
        # Write content to the file
        file_path.write_text(content)
    except IOError as e:
        raise IOError(f"An error occurred while writing to the file: {e}")

def read_file_content(file_path: Path) -> str:
    """
    Reads the content of the specified file.

    Args:
        file_path (Path): The path of the file to read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        # Read content from the file
        return file_path.read_text()
    except IOError as e:
        raise IOError(f"An error occurred while reading the file: {e}")

def main() -> None:
    """
    Main function to demonstrate file creation and reading.
    """
    # Define the file path
    file_path = Path("example.txt")
    
    # Content to write
    content = "Hello, World!\nThis is a sample file."

    # Create the file with content
    try:
        create_file_with_content(file_path, content)
        print(f"File created: {file_path}")
    except Exception as e:
        print(e)

    # Read the content of the file
    try:
        file_content = read_file_content(file_path)
        print(f"File content:\n{file_content}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()