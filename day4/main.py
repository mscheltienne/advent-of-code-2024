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
            if data[i + k * offset[0], j + k * offset[1]] != letter:
                break
        else:
            count += 1
    return count


total = get_number_of_word(data)
print(f"The total number of XMAS is {total}.")
