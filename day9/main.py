from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    data: str = fid.read().strip()
    data: NDArray[np.int8] = np.array([int(char) for char in data], dtype=np.int8)


# %% part 1
def compress(data: NDArray[np.int8]) -> NDArray[np.int32]:
    """Compress the data sequence."""
    filesizes = data[::2]
    free_spaces = data[1::2]
    total_fsize = np.sum(filesizes)
    # initialize the result with nan to represent free space
    result = [0] * filesizes[0]
    filesizes = filesizes[1:]
    assert len(filesizes) == len(free_spaces)  # sanity-check
    for k, (fsize, ssize) in enumerate(zip(filesizes, free_spaces, strict=True)):
        result.extend([np.nan] * ssize)
        result.extend([k + 1] * fsize)
    result = np.array(result, dtype=np.float32)
    # compaction logic
    while True:
        leftmost_free = np.where(np.isnan(result))[0][0]
        if leftmost_free == total_fsize:
            break
        rightmost_file = np.where(~np.isnan(result))[0][-1]
        result[leftmost_free] = result[rightmost_file]
        result[rightmost_file] = np.nan
    return result[:total_fsize].astype(np.int32)


def checksum(compressed: NDArray[np.int32]) -> int:
    """Calculate the checksum of the compressed data."""
    total_checksum = 0
    for k, file_id in enumerate(compressed):
        total_checksum += k * int(file_id)
    return total_checksum


compressed = compress(data)
total = checksum(compressed)
print(f"The total checksum is: {total}.")
