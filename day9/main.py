from __future__ import annotations

from itertools import groupby
from operator import itemgetter
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

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


# %% part 2
def compress(data: NDArray[np.int8]) -> NDArray[np.float32]:
    """Compress the data sequence without fragmentation."""
    filesizes = data[::2]
    free_spaces = data[1::2]
    # initialize the result with nan to represent free space
    result = [0] * filesizes[0]
    filesizes = filesizes[1:]
    assert len(filesizes) == len(free_spaces)  # sanity-check
    file_idx = []  # initial position of each file in result, except the first (ID=0)
    for k, (fsize, ssize) in enumerate(zip(filesizes, free_spaces, strict=True)):
        result.extend([np.nan] * ssize)
        result.extend([k + 1] * fsize)
        file_idx.append(slice(len(result) - int(fsize), len(result)))
    result = np.array(result, dtype=np.float32)
    # compaction logic
    for fsize, fpos in zip(filesizes[::-1], file_idx[::-1], strict=True):
        left_free_spaces = np.where(np.isnan(result[: fpos.start]))[0]
        for group in _consecutive_groups(left_free_spaces):
            group = list(group)
            if len(group) >= fsize:
                result[group[:fsize]] = result[fpos]
                result[fpos] = np.nan
                break
    return result


def _consecutive_groups(
    iterable: NDArray[np.int64], ordering: Callable = lambda x: x
) -> Generator:
    """Yield groups of consecutive items using itertools.groupby."""
    for _, g in groupby(enumerate(iterable), key=lambda x: x[0] - ordering(x[1])):
        yield map(itemgetter(1), g)


def checksum(compressed: NDArray[np.float32]) -> int:
    """Calculate the checksum of the compressed data."""
    total_checksum = 0
    for k, file_id in enumerate(compressed):
        if not np.isnan(file_id):
            total_checksum += k * int(file_id)
    return total_checksum


compressed = compress(data)
total = checksum(compressed)
print(f"The total checksum is: {total}.")
