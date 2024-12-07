from __future__ import annotations

from dataclasses import dataclass
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
_MOVEMENTS: dict[int, tuple[int, int]] = {
    2: (-1, 0),
    3: (0, 1),
    4: (1, 0),
    5: (0, -1),
}


def walk_path(
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


positions = walk_path(data, x, y, orientation)
print(f"The guard walked on {len(positions)} positions.")


# %% part 2
@dataclass(frozen=True)
class Node:
    """A node representing the guard position/orientation and the map state."""

    x: int
    y: int
    orientation: int
    x_obstacle: int | None
    y_obstacle: int | None


def turn_right(orientation: int) -> int:
    """Turn the guard to the right."""
    return {2: 3, 3: 4, 4: 5, 5: 2}[orientation]


def in_bounds(data: NDArray[np.bool_], x: int, y: int) -> bool:
    """Check if the guard is still on the map."""
    rows, cols = data.shape
    return 0 <= x < rows and 0 <= y < cols


def can_turn_right(data: NDArray[np.bool], x: int, y: int, orientation: int) -> bool:
    """Check if the guard can turn right."""
    dx, dy = _MOVEMENTS[turn_right(orientation)]
    nextx, nexty = x + dx, y + dy
    if not in_bounds(data, nextx, nexty):
        return False
    return not data[nextx, nexty]


def walk_path(
    G: nx.DiGraph,
    data: NDArray[np.bool],
    x: int,
    y: int,
    orientation: int,
    x_obstacle: int,
    y_obstacle: int,
) -> None:
    """Walk down a path and add the corresponding nodes to the graph."""
    for _ in range(2):  # find the next position
        dx, dy = _MOVEMENTS[orientation]
        nextx, nexty = x + dx, y + dy
        if not in_bounds(data, nextx, nexty):
            return
        if data[nextx, nexty]:  # obstacle in the next location
            new_orientation = turn_right(orientation)
            G.add_edge(
                Node(x, y, orientation, x_obstacle, y_obstacle),
                Node(x, y, new_orientation, x_obstacle, y_obstacle),
            )
            orientation = new_orientation
            continue
        break
    next_node = Node(nextx, nexty, orientation, x_obstacle, y_obstacle)
    if next_node not in G:
        G.add_edge(Node(x, y, orientation, x_obstacle, y_obstacle), next_node)
        walk_path(G, data, nextx, nexty, orientation, x_obstacle, y_obstacle)


def build_graph(data: NDArray[np.bool], x: int, y: int, orientation: int) -> nx.DiGraph:
    """Create a graph reprensenting the guard pattern.

    Each node represents a (x, y, orientation) tuple.
    Each edge represents a forward movement of the guard.
    """
    G = nx.DiGraph()
    G.add_node(Node(x, y, orientation, None, None))  # starting position
    # walk down the normal path, and at every step branch out between the normal path
    # and the one where the guard turns right due to a new obstacle in front of her.
    while True:
        dx, dy = _MOVEMENTS[orientation]
        nextx, nexty = x + dx, y + dy  # next position
        if not in_bounds(data, nextx, nexty):
            break
        elif data[nextx, nexty]:
            new_orientation = turn_right(orientation)
            G.add_edge(
                Node(x, y, orientation, None, None),
                Node(x, y, new_orientation, None, None),
            )
            orientation = new_orientation
            continue
        # move forward and add the node (x, y, o) corresponding to the normal path
        G.add_edge(
            Node(x, y, orientation, None, None),
            Node(nextx, nexty, orientation, None, None),
        )
        # check if the guard can turn right, in which case let's try to add an obstacle
        # in front of her to branch out.
        if can_turn_right(data, x, y, orientation):
            data[nextx, nexty] = True
            walk_path(G, data, x, y, orientation, nextx, nexty)
            data[nextx, nexty] = False
        x, y = nextx, nexty
    return G


G = build_graph(data, x, y, orientation)
nx.draw(G)
cycles = nx.simple_cycles(G)
print(f"The guard walked on {len(list(cycles))} cycles.")
