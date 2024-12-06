from __future__ import annotations

import re
from pathlib import Path

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    data: str = fid.read()


# %% part 1
def get_multiplication_result(data: str) -> int:
    """Get the multiplication value after parsing the corrupted memory."""
    pattern = re.compile(r"mul\(\d+,\d+\)")
    total = 0
    for elt in re.findall(pattern, data):
        a, b = map(int, re.findall(r"\d+", elt))
        total += a * b
    return total


total = get_multiplication_result(data)
print(f"The total multiplication result is {total}.")


# %% part 2
def get_multiplication_result_with_conditionals(data: str) -> int:
    """Get the multiplication value after parsing the corrupted memory."""
    pattern = re.compile(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))")
    total = 0
    enabled = True
    for elt in re.findall(pattern, data):
        if enabled and elt[0]:
            a, b = map(int, re.findall(r"\d+", elt[0]))
            total += a * b
        elif enabled and elt[2]:
            enabled = False
        elif not enabled and elt[1]:
            enabled = True
    return total


total = get_multiplication_result_with_conditionals(data)
print(f"The total multiplication result is {total}.")
