from __future__ import annotations

from itertools import product
from pathlib import Path

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    data: list[str] = fid.readlines()
data: list[list[str]] = [elt.split(":") for elt in data]
data: list[tuple[int, list[int]]] = [
    (int(elt[0]), [int(e) for e in elt[1].strip().split(" ")]) for elt in data
]


# %% part 1
def is_valid(equation: tuple[int, list[int]]) -> bool:
    """Check if an equation is valid."""
    result = equation[0]
    numbers = equation[1]
    if len(numbers) == 1:
        return result == numbers[0]
    for ops in product(["+", "*"], repeat=len(numbers) - 1):
        value = numbers[0]
        for op, num in zip(ops, numbers[1:]):
            if op == "+":
                value += num
            elif op == "*":
                value *= num
        if value == result:
            return True
    return False


total = sum(equation[0] for equation in data if is_valid(equation))
print(f"The sum of all valid equation's result is {total}.")
