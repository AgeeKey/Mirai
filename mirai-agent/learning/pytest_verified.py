"""
pytest - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-22T11:17:52.387946

This code has been verified by MIRAI's NASA-level learning system.
"""

import pytest

def divide(a: float, b: float) -> float:
    """
    Divides two numbers.

    Parameters:
    a (float): The numerator.
    b (float): The denominator.

    Returns:
    float: The result of the division.

    Raises:
    ValueError: If the denominator is zero.
    """
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b

def test_divide():
    """Tests the divide function."""
    # Test valid division
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    # Test division by zero
    with pytest.raises(ValueError, match="Denominator cannot be zero."):
        divide(1, 0)

if __name__ == "__main__":
    pytest.main()