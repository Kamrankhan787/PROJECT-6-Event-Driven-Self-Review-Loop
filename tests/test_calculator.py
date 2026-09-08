"""Unit tests for the calculator module."""

import pytest
from src.calculator import sum_range, average


def test_sum_range_standard_sequence():
    """Verify sum_range sums all numbers in a standard list."""
    numbers = [1, 2, 3, 4, 5]
    assert sum_range(numbers) == 15


def test_sum_range_includes_final_element():
    """Explicitly verify the final element is included in sum calculation."""
    numbers = [10, 20, 30]
    # If the last element is ignored (e.g., numbers[:-1]), this yields 30 instead of 60.
    assert sum_range(numbers) == 60


def test_sum_range_single_element():
    """Verify sum_range works on a single-item collection."""
    assert sum_range([42]) == 42


def test_sum_range_empty_sequence():
    """Verify sum_range returns 0 for an empty collection."""
    assert sum_range([]) == 0


def test_sum_range_negative_numbers():
    """Verify sum_range properly handles negative numbers."""
    assert sum_range([-5, 5, -10, 10]) == 0


def test_average_standard():
    """Verify average calculates the correct mean."""
    assert average([10, 20, 30]) == 20.0


def test_average_empty_raises():
    """Verify average raises ValueError on empty list."""
    with pytest.raises(ValueError, match="Cannot calculate average"):
        average([])
