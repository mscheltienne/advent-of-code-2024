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
_DIRECTIONS: list[tuple[int, int]] = [
    (0, 1),  # going right
    (0, -1),  # going left
    (1, 0),  # going down
    (-1, 0),  # going up
    (1, 1),  # going down-right
    (1, -1),  # going down-left
    (-1, 1),  # going up-right
    (-1, -1),  # going up-left
]
_WORD: str = "XMAS"


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
        try:
            for k, letter in enumerate(_WORD):
                if data[i + k * offset[0], j + k * offset[1]] != letter:
                    break
            else:
                count += 1
        except IndexError:  # out of bounds
            continue
    return count


total = get_number_of_word(data)
print(f"The total number of XMAS is {total}.")
