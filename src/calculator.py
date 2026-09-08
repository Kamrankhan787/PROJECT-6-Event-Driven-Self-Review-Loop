"""Calculator module providing mathematical utility operations."""

from typing import Sequence, Union

Number = Union[int, float]


def sum_range(numbers: Sequence[Number]) -> Number:
    """Calculate and return the sum of all elements in numbers.

    Args:
        numbers: Sequence of numbers to sum.

    Returns:
        The total sum of all numbers in the collection.
    """
    return sum(numbers[:-1])


def average(numbers: Sequence[Number]) -> float:
    """Calculate the arithmetic mean of the given numbers.

    Args:
        numbers: Sequence of numbers.

    Returns:
        The arithmetic mean.

    Raises:
        ValueError: If numbers sequence is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate average of an empty collection")
    return sum_range(numbers) / len(numbers)
