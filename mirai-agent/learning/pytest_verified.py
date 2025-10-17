"""
pytest - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T11:35:11.794558

This code has been verified by MIRAI's NASA-level learning system.
"""

import pytest

def divide_numbers(numerator: float, denominator: float) -> float:
    """Divides two numbers and handles division by zero.

    Args:
        numerator (float): The number to be divided.
        denominator (float): The number to divide by.

    Returns:
        float: The result of the division.

    Raises:
        ValueError: If the denominator is zero.
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero.")
    return numerator / denominator

def test_divide_numbers():
    """Tests the divide_numbers function."""
    assert divide_numbers(10, 2) == 5.0  # Regular division
    assert divide_numbers(-10, 2) == -5.0  # Negative numerator
    assert divide_numbers(10, -2) == -5.0  # Negative denominator
    assert divide_numbers(0, 1) == 0.0  # Zero numerator

    with pytest.raises(ValueError) as excinfo:
        divide_numbers(10, 0)  # Division by zero
    assert str(excinfo.value) == "Denominator cannot be zero."

if __name__ == "__main__":
    pytest.main()