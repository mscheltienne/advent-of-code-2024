from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
char_to_num: dict[str, int] = {".": 0}
with open(fname) as fid:
    data: list[str] = [line.strip() for line in fid.readlines()]
data_numerical: list[list[int]] = []
for line in data:
    new_char = set(line).difference(set(char_to_num))
    for char in new_char:
        char_to_num[char] = len(char_to_num)
    line = [char_to_num[char] for char in line]
    data_numerical.append(line)
data: NDArray[np.int8] = np.array(data_numerical, dtype=np.int8)


# %% part 1
def find_antinodes(
    data: NDArray[np.int8], antenna1: NDArray[np.int8], antenna2: NDArray[np.int8]
) -> list[tuple[int, int]]:
    """Find the antinodes of a given pair of antennas."""
    x1, y1 = antenna1
    x2, y2 = antenna2
    # compute the vector from antenna1 to antenna2
    vector = np.array([x2 - x1, y2 - y1], dtype=np.int8)  # (dx, dy)
    # compute the position of the 2 antinodes
    antinodes = [antenna1 - vector, antenna2 + vector]
    return [tuple(antinode) for antinode in antinodes if in_bounds(data, *antinode)]


def in_bounds(data: NDArray[np.int8], x: int, y: int) -> bool:
    """Check if the antinode is still on the map."""
    rows, cols = data.shape
    return 0 <= x < rows and 0 <= y < cols


def find_antinodes_for_frequency(
    data: NDArray[np.int8], freq: int
) -> set[tuple[int, int]]:
    """Find the antinodes for a given frequency."""
    antinodes = set()
    # store the coordinates of the antennas at the frequency freq in a 2D array of shape
    # (n_antennas, 2) where the first column is the x coordinate and the second column
    # is the y coordinate.
    antennas = np.vstack(np.where(data == freq), dtype=np.int8).T
    for antenna1, antenna2 in combinations(antennas, 2):
        new_antinodes = find_antinodes(data, antenna1, antenna2)
        antinodes.update(set(new_antinodes))
    return set(antinodes)


def find_antinodes_for_all_frequencies(data: NDArray[np.int8]) -> list[tuple[int, int]]:
    """Find the antinodes for all frequencies."""
    antinodes = set()
    frequencies = np.unique(data)
    for k, freq in enumerate(frequencies):
        if freq == 0:  # skip the empty space
            continue
        print(f"{k} / {frequencies.size - 1}: Finding antinodes for frequency {freq}.")
        antinodes.update(find_antinodes_for_frequency(data, freq))
    return antinodes


total = len(find_antinodes_for_all_frequencies(data))
print(f"The total number of antinodes is {total}.")


# %% part 2
def find_antinodes(  # noqa: F811
    data: NDArray[np.int8], antenna1: NDArray[np.int8], antenna2: NDArray[np.int8]
) -> list[tuple[int, int]]:
    """Find the antinodes of a given pair of antennas, including harmonics."""
    x1, y1 = antenna1
    x2, y2 = antenna2
    # compute the vector from antenna1 to antenna2
    vector = np.array([x2 - x1, y2 - y1], dtype=np.int8)  # (dx, dy)
    # compute the position of the antinodes
    antinodes = [tuple(antenna1), tuple(antenna2)]
    pos = antenna1
    while True:  # antinodes for antenna1
        antinode = pos - vector
        if not in_bounds(data, *antinode):
            break
        antinodes.append(tuple(antinode))
        pos = antinode
    pos = antenna2
    while True:  # antinodes for antenna2
        antinode = pos + vector
        if not in_bounds(data, *antinode):
            break
        antinodes.append(tuple(antinode))
        pos = antinode
    return antinodes


total = len(find_antinodes_for_all_frequencies(data))
print(f"The total number of antinodes is {total}.")
