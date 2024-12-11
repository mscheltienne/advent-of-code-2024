from __future__ import annotations

from collections import Counter
from functools import cache
from pathlib import Path

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    data: list[int] = [int(elt) for elt in fid.read().strip().split(" ")]


# %% part 1
def process_stone(stone: int) -> list[int]:
    """Process the given stone and figure out what happens to it."""
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone = str(stone)
        assert stone[0] != "0"  # sanity-check, a stone can't start with 0
        return [int(stone[: len(stone) // 2]), int(stone[len(stone) // 2 :])]
    else:
        return [stone * 2024]


def process_blink(data: list[int]) -> list[int]:
    """Process a blink iteration on the list of stones."""
    result = []
    for stone in data:
        new_stone = process_stone(stone)
        result.extend(new_stone)
    return result


def count_stones_after_n_blinks(data: list[int], n: int) -> int:
    """Count the number of stones after n blinks."""
    for k in range(n):
        print(f"Processing blink {k + 1} / {n}..")
        data = process_blink(data)
    return len(data)


total = count_stones_after_n_blinks(data, 25)
print(f"Total stones after 25 blinks: {total}.")


# %% part 2
@cache
def process_stone(stone: int) -> list[int]:  # noqa: F811
    """Process the given stone and figure out what happens to it."""
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone = str(stone)
        assert stone[0] != "0"  # sanity-check, a stone can't start with 0
        return [int(stone[: len(stone) // 2]), int(stone[len(stone) // 2 :])]
    else:
        return [stone * 2024]


def process_blink(stone_counts: Counter[int]) -> Counter[int]:  # noqa: F811
    """Process a blink iteration on the list of stones."""
    counts = Counter()
    for stone, count in stone_counts.items():
        transformed_stones = process_stone(stone)
        for new_stone in transformed_stones:
            counts[new_stone] += count
    return counts


def count_stones_after_n_blinks(data: list[int], n: int) -> int:  # noqa: F811
    """Count the number of stones after n blinks."""
    stone_counts = Counter(data)
    for k in range(n):
        print(f"Processing blink {k + 1} / {n}..")
        stone_counts = process_blink(stone_counts)
    return sum(stone_counts.values())


total = count_stones_after_n_blinks(data, 75)
print(f"Total stones after 75 blinks: {total}.")
