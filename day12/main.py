from __future__ import annotations

from itertools import product
from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
char_to_num: dict[str, int] = dict()
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
def build_graph() -> nx.Graph:
    """Build a graph representation of the map."""
    G = nx.Graph()
    rows, cols = data.shape
    for x, y in product(range(rows), range(cols)):
        G.add_node((x, y))
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if in_bounds(data, new_x, new_y) and data[new_x, new_y] == data[x, y]:
                G.add_edge((x, y), (new_x, new_y))
    return G


def in_bounds(data: NDArray[np.int8], x: int, y: int) -> bool:
    """Check if the antinode is still on the map."""
    rows, cols = data.shape
    return 0 <= x < rows and 0 <= y < cols


def estimate_fence_cost(G: nx.Graph) -> int:
    """Estimate the cost of the fence."""
    return sum(
        len(elt) * sum(4 - G.degree[node] for node in elt)
        for elt in nx.connected_components(G)
    )


G = build_graph()
total = estimate_fence_cost(G)

# %% part 2
