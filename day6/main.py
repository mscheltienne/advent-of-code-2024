from __future__ import annotations

from itertools import cycle
from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx
import numpy as np

if TYPE_CHECKING:
    from collections.abc import Generator

    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "example.txt"
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


def walk_pattern(
    data: NDArray[np.bool], x: int, y: int, direction: int
) -> set[tuple[int, int]]:
    """Walk the guard pattern and list the positions visited."""
    direction_cycle: Generator = cycle(_DIRECTIONS)
    while next(direction_cycle) != direction:
        pass
    positions = {(x, y)}
    while True:
        dx, dy = _DIRECTIONS[direction]
        nextx, nexty = x + dx, y + dy  # next position
        if nextx < 0 or data.shape[0] <= nextx or nexty < 0 or data.shape[1] <= nexty:
            break  # out of the map
        elif data[nextx, nexty]:
            direction = next(direction_cycle)
            continue
        # move forward and record the guard position
        x, y = nextx, nexty
        positions.add((x, y))
    return positions


positions = walk_pattern(data, x, y, orientation)
print(f"The guard walked on {len(positions)} positions.")


# %% part 2
def build_graph(data: NDArray[np.bool], x: int, y: int, direction: int) -> nx.DiGraph:
    """Create a graph reprensenting the guard pattern.

    Each node represents a (x, y, orientation) tuple.
    Each edge represents a forward movement of the guard.
    """
    direction_cycle: Generator = cycle(_DIRECTIONS)
    while next(direction_cycle) != direction:
        pass
    G = nx.DiGraph()
    G.add_node((x, y, direction))
    while True:
        dx, dy = _DIRECTIONS[direction]
        nextx, nexty = x + dx, y + dy  # next position
        if nextx < 0 or data.shape[0] <= nextx or nexty < 0 or data.shape[1] <= nexty:
            break  # out of the map
        elif data[nextx, nexty]:
            direction = next(direction_cycle)
            continue
        # move forward and add the node (x, y, o) and its edges
        x, y = nextx, nexty
        stop = (x, y, direction) in G
        G.add_edge((x - dx, y - dy, direction), (x, y, direction))
        if stop:
            break
    return G
