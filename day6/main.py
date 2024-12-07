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
    """A node representing the guard position/orientation."""

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


def walk_path(data: NDArray[np.bool], node: Node) -> nx.DiGraph:
    """Walk down a path and add the corresponding nodes to the graph."""
    G = nx.DiGraph()
    G.add_node(node)  # starting position
    visited = {node}
    while True:
        dx, dy = _MOVEMENTS[node.orientation]
        nextx, nexty = node.x + dx, node.y + dy
        if not in_bounds(data, nextx, nexty):
            break
        if data[nextx, nexty]:
            new_orientation = turn_right(node.orientation)
            new_node = Node(node.x, node.y, new_orientation)
            G.add_edge(node, new_node)
            visited.add(new_node)
            node = new_node
            continue
        new_node = Node(nextx, nexty, node.orientation)
        G.add_edge(node, new_node)
        if new_node in visited:
            break
        visited.add(new_node)
        node = new_node
    return G


def search_loops(data: NDArray[np.bool], node_start: Node):
    """Search for loops when adding one obstacle to the map."""
    pos = walk_normal_path(data, node_start.x, node_start.y, node_start.orientation)
    pos.remove((node_start.x, node_start.y))
    loops = dict()
    for k, (x, y) in enumerate(pos):
        print(f"Iteration {k} for position {(x, y)}")
        data_ = data.copy()
        data_[x, y] = True
        G = walk_path(data_, node_start)
        cycles = list(nx.simple_cycles(G))
        if cycles:
            loops[(x, y)] = cycles
    return loops


loops = search_loops(data, Node(x, y, orientation))
print(f"The number of loops is {len(loops)}.")
