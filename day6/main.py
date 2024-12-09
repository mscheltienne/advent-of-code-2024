from __future__ import annotations

from dataclasses import dataclass
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
_MOVEMENTS: dict[int, tuple[int, int]] = {
    2: (-1, 0),
    3: (0, 1),
    4: (1, 0),
    5: (0, -1),
}


def walk_normal_path(
    data: NDArray[np.bool], x: int, y: int, orientation: int
) -> set[tuple[int, int]]:
    """Walk the guard pattern and list the positions visited."""
    orientation_cycle: Generator = cycle(_MOVEMENTS)
    while next(orientation_cycle) != orientation:
        pass
    positions = {(x, y)}
    while True:
        dx, dy = _MOVEMENTS[orientation]
        nextx, nexty = x + dx, y + dy  # next position
        if nextx < 0 or data.shape[0] <= nextx or nexty < 0 or data.shape[1] <= nexty:
            break  # out of the map
        elif data[nextx, nexty]:
            orientation = next(orientation_cycle)
            continue
        # move forward and record the guard position
        x, y = nextx, nexty
        positions.add((x, y))
    return positions


positions = walk_normal_path(data, x, y, orientation)
print(f"The guard walked on {len(positions)} positions.")


# %% part 2
@dataclass(frozen=True)
class Node:
    """A node representing the guard position/orientation.

    Parameters
    ----------
    x : int
        The x-coordinate of the guard.
    y : int
        The y-coordinate of the guard.
    orientation : int
        The orientation of the guard.
        * 2: facing up
        * 3: facing right
        * 4: facing down
        * 5: facing left
    """

    # another representation of the guard position and orientation could be his position
    # on the 2D complex plane. Then, a change of orientation by 90° to the right
    # corresponds to a rotation (multiplication) by the complex number 1j.

    x: int
    y: int
    orientation: int


def in_bounds(data: NDArray[np.bool_], x: int, y: int) -> bool:
    """Check if the guard is still on the map."""
    rows, cols = data.shape
    return 0 <= x < rows and 0 <= y < cols


def turn_right(orientation: int) -> int:
    """Turn the guard to the right."""
    return {2: 3, 3: 4, 4: 5, 5: 2}[orientation]


def walk_path(data: NDArray[np.bool], node: Node) -> bool:
    """Walk down a path and search for loops."""
    visited = {node}
    while True:
        dx, dy = _MOVEMENTS[node.orientation]
        nextx, nexty = node.x + dx, node.y + dy
        if not in_bounds(data, nextx, nexty):
            return False
        if data[nextx, nexty]:
            new_orientation = turn_right(node.orientation)
            new_node = Node(node.x, node.y, new_orientation)
            if new_node in visited:
                return True
            visited.add(new_node)
            node = new_node
            continue
        new_node = Node(nextx, nexty, node.orientation)
        if new_node in visited:
            return True
        visited.add(new_node)
        node = new_node


def search_loops(data: NDArray[np.bool], node_start: Node) -> int:
    """Search for loops when adding one obstacle to the map."""
    pos = walk_normal_path(data, node_start.x, node_start.y, node_start.orientation)
    pos.remove((node_start.x, node_start.y))
    n_loops = 0
    for k, (x, y) in enumerate(pos):
        print(f"Iteration {k + 1} / {len(pos)} for position {(x, y)}.")
        data[x, y] = True
        loop = walk_path(data, node_start)
        data[x, y] = False
        n_loops += loop
    return n_loops


n_loops = search_loops(data, Node(x, y, orientation))
print(f"The number of loops is {n_loops}.")
