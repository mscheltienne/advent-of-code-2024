from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
data: NDArray[np.int32] = np.loadtxt(fname, dtype=np.int32)  # shape of (1000, 2)


# %% part 1
def get_distances(data: NDArray[np.int32]) -> int:
    """Get the total distances."""
    distances = np.abs(np.sort(data[:, 1]) - np.sort(data[:, 0]))
    return np.sum(distances)


total = get_distances(data)
print(f"The total distance is {total}.")


# %% part 2
def get_similarity(data: NDArray[np.int32]) -> int:
    """Get the similarity score."""
    intersection = np.intersect1d(data[:, 0], data[:, 1])
    total = 0
    for elt in intersection:
        total += np.where(data[:, 1] == elt)[0].size * elt
    return total


total = get_similarity(data)
print(f"The total similarity score is {total}.")
