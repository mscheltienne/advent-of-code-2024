from __future__ import annotations

from itertools import cycle
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Generator

    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
char_to_num: dict[str, int] = {".": 0, "#": 1, "^": 2, ">": 3, "v": 4, "<": 5}
with open(fname) as fid:
    data: list[list[int]] = [
        [char_to_num[char] for char in line.strip()] for line in fid.readlines()
    ]
# find the position and orientation of the guard and convert data to a binary matrix
data: NDArray[np.int8] = np.array(data, dtype=np.int8)
x, y = np.where(data > 1)
x = int(x[0])
y = int(y[0])
orientation: int = int(data[x, y])
data[x, y] = 0
data: NDArray[np.bool] = data.astype(np.bool)

# %% part 1
_DIRECTIONS: dict[int, tuple[int, int]] = {
    2: (-1, 0),
    3: (0, 1),
    4: (1, 0),
    5: (0, -1),
}
_DIRECTIONS_CYCLE: Generator = cycle(_DIRECTIONS)


def walk_pattern(
    data: NDArray[np.bool], x: int, y: int, direction: int
) -> set[tuple[int, int]]:
    """Walk the guard pattern and list the positions visited."""
    while next(_DIRECTIONS_CYCLE) != direction:
        pass
    positions = {(x, y)}
    while True:
        dx, dy = _DIRECTIONS[direction]
        nx, ny = x + dx, y + dy  # next position
        if nx < 0 or data.shape[0] <= nx or ny < 0 or data.shape[1] <= ny:
            break
        elif data[nx, ny]:
            direction = next(_DIRECTIONS_CYCLE)
            continue
        # move forward and record the guard position
        x, y = nx, ny
        positions.add((x, y))
    return positions


positions = walk_pattern(data, x, y, orientation)
print(f"The guard walked on {len(positions)} positions.")

# %% part 2
