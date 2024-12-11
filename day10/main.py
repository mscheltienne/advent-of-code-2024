from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    data: NDArray[np.int8] = np.array(
        [[int(elt) for elt in line.strip()] for line in fid.readlines()], dtype=np.int8
    )


# %% part 1
def build_graph(
    data: NDArray[np.int8], trailheads: list[tuple[int, int]]
) -> nx.DiGraph:
    """Build the graph containing the trails on the map."""
    G = nx.DiGraph()
    for x, y in trailheads:
        assert data[x, y] == 0  # sanity-check
        add_edges_on_path(G, data, x, y)
    return G


def add_edges_on_path(G: nx.DiGraph, data: NDArray[np.int8], x: int, y: int):
    """Add all edges next to (x, y) on the trail."""
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        if in_bounds(data, new_x, new_y) and data[new_x, new_y] == data[x, y] + 1:
            G.add_edge((x, y), (new_x, new_y))
            add_edges_on_path(G, data, new_x, new_y)


def in_bounds(data: NDArray[np.int8], x: int, y: int) -> bool:
    """Check if the position is on the map."""
    rows, cols = data.shape
    return 0 <= x < rows and 0 <= y < cols


def measure_score(data: NDArray[np.int8]) -> int:
    """Measure the total score of the trails on the map."""
    trailheads = list(zip(*np.where(data == 0)))
    trailends = list(zip(*np.where(data == 9)))
    G = build_graph(data, trailheads)
    total_score = 0
    for trailhead in trailheads:
        score = 0
        for trailend in trailends:
            if nx.has_path(G, trailhead, trailend):
                score += 1
        total_score += score
    return total_score


total = measure_score(data)
print(f"The total score of the trailheads is: {total}.")


# %% part 2
def measure_rating(data: NDArray[np.int8]) -> int:
    """Measure the total rating of the trails on the map."""
    trailheads = list(zip(*np.where(data == 0)))
    trailends = list(zip(*np.where(data == 9)))
    G = build_graph(data, trailheads)
    total_rating = 0
    for trailhead in trailheads:
        rating = 0
        for trailend in trailends:
            rating += len(list(nx.all_simple_paths(G, trailhead, trailend)))
        total_rating += rating
    return total_rating


total = measure_rating(data)
print(f"The total rating of the trailheads is: {total}.")
