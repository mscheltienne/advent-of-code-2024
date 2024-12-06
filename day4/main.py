from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    data: list[str] = fid.readlines()
# array of shape (140, 140)
data = np.array([list(elt.strip()) for elt in data])

# %% part 1
# fmt: off
_DIRECTIONS: list[tuple[int, int]] = [
    (0, 1),   # right
    (0, -1),  # left
    (1, 0),   # down
    (-1, 0),  # up
    (1, 1),   # down-right
    (1, -1),  # down-left
    (-1, 1),  # up-right
    (-1, -1), # up-left
]
_WORD: str = "XMAS"
# fmt: on


def get_number_of_word(data: NDArray) -> int:
    """Get the number of times the word appears in the data."""
    total = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j] == _WORD[0]:
                total += _count_around_first_letter(data, i, j)
    return total


def _count_around_first_letter(data: NDArray, i: int, j: int) -> int:
    """Count the number of patterns at that X location."""
    count = 0
    for offset in _DIRECTIONS:
        if not 0 <= i + (len(_WORD) - 1) * offset[0] < data.shape[0]:
            continue
        if not 0 <= j + (len(_WORD) - 1) * offset[1] < data.shape[1]:
            continue
        for k, letter in enumerate(_WORD):
            if k == 0:
                continue  # skip the first letter which is already tested
            if data[i + k * offset[0], j + k * offset[1]] != letter:
                break
        else:
            count += 1
    return count


total = get_number_of_word(data)
print(f"The total number of XMAS is {total}.")


# %% part 2
_RING_ROWS = np.array([0, 0, 0, 1, 2, 2, 2, 1])
_RINGS_COLS = np.array([0, 1, 2, 2, 2, 1, 0, 0])


def get_number_of_x_mas(data: NDArray) -> int:
    """Get the number of X-mas, i.e. of MAS formning an X."""
    total = 0
    for i in range(1, data.shape[0] - 1):
        for j in range(1, data.shape[1] - 1):
            if data[i, j] == "A":
                total += _count_around_A(data[i - 1 : i + 2, j - 1 : j + 2])
    return total


def _count_around_A(data: NDArray) -> int:
    """Count the number of patterns at that A location."""
    assert data.shape == (3, 3)  # sanity-check
    count = 0
    for _ in range(4):
        ring_values = data[_RING_ROWS, _RINGS_COLS]
        rotated_values = np.roll(ring_values, 2)
        data[_RING_ROWS, _RINGS_COLS] = rotated_values
        if _is_pattern(data):
            count += 1
    return count


def _is_pattern(data: NDArray) -> bool:
    """Check if the data is the pattern."""
    if (
        data[0, 0] == "M"
        and data[-1, 0] == "M"
        and data[0, -1] == "S"
        and data[-1, -1] == "S"
    ):
        return True
    return False


total = get_number_of_x_mas(data)
print(f"The total number of X-MAS is {total}.")
