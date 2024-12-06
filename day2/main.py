from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
reports: list[list[int]] = []
size: int = 0
with open(fname) as fid:
    for line in fid:
        line = line.strip().split(" ")
        report = [int(elt) for elt in line]
        reports.append(report)
        size = max(size, len(report))

# array of shape (1000, 8)
data: NDArray[np.float16] = np.full((len(reports), size), np.nan, dtype=np.float16)
for i, report in enumerate(reports):
    data[i, : len(report)] = report


# %% part 1
def get_safe_reports(data: NDArray[np.float16]) -> int:
    """Get the number of safe reports.

    A report is safe if all elements are either increasing or decreasing by 1-3.
    """
    safe = 0
    diff = np.diff(data, axis=1)
    for elt in diff:  # array of shape (n_levels - 1,) containing nans
        elt = elt[~np.isnan(elt)]
        # first check monotonicity, excluding 0 (same number) and then check the step
        if (np.all(0 < elt) or np.all(elt < 0)) and not np.any(3 < np.abs(elt)):
            safe += 1
    return safe


total = get_safe_reports(data)
print(f"The number of safe reports is {total}.")


# %% part 2
def get_safe_reports_with_dampener(data: NDArray[np.float16]) -> int:
    """Get the number of safe reports with a problem dampener.

    The same rules applies, but now if removing one level from the reports makes it safe
    then the report is considered safe.
    """
    safe = 0
    for report in data:
        if _is_safe_with_dampener(report):
            safe += 1
    return safe


def _is_safe(report: NDArray[np.float16]) -> bool:
    """Check if a report is safe."""
    diff = np.diff(report[~np.isnan(report)])
    if not (np.all(diff > 0) or np.all(diff < 0)):  # check monotonicity
        return False
    if np.any(3 < np.abs(diff)):
        return False
    return True


def _is_safe_with_dampener(report: NDArray[np.foat16]) -> bool:
    """Check if a report is safe with the problem dampener."""
    if _is_safe(report):
        return True
    # let's try to remove one level
    report = report[~np.isnan(report)]
    for k in range(len(report)):
        new_report = np.delete(report, k)
        if _is_safe(new_report):
            return True
    return False


total = get_safe_reports_with_dampener(data)
print(f"The number of safe reports is {total}.")
