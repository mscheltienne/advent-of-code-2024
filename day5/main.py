from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    data: list[str] = fid.readlines()

# split the input between the page ordering rules and the updates.
split: int = data.index("\n")
rules: NDArray[np.int8] = np.array(
    [[int(page) for page in elt.strip().split("|")] for elt in data[:split]],
    dtype=np.int8,
)
updates: list[list[int]] = [
    [int(page) for page in elt.strip().split(",")] for elt in data[split + 1 :]
]


# %% part 1
def find_middle_page_of_updates_correctly_ordered(
    updates: list[list[int]], rules: NDArray[np.int8]
) -> list[int]:
    """Find the middle page of the correctly ordered updates."""
    middle_pages = []
    for update in updates:
        valid = True
        for k, page in enumerate(update):
            if k == len(update) - 1:  # if we got to the last page, the update is valid
                middle_pages.append(_get_middle_page(update))
                break
            if page not in rules[:, 1]:
                continue
            idx = np.where(rules[:, 1] == page)[0]
            for rule in rules[idx, 0]:
                if rule in update[k + 1 :]:
                    valid = False
                    break
            if not valid:
                break
    return middle_pages


def _get_middle_page(update: list[int]) -> int:
    """Get the middle page of an update."""
    return update[len(update) // 2]


middle_pages = find_middle_page_of_updates_correctly_ordered(updates, rules)
print(f"The sum of the middle pages is {np.sum(middle_pages)}.")


# %% part 2
def get_updates_incorrectly_ordered(
    updates: list[list[int]], rules: NDArray[np.int8]
) -> list[list[int]]:
    """Find the incorrectly ordered updates."""
    invalids = []
    for update in updates:
        valid = True
        for k, page in enumerate(update):
            if k == len(update) - 1:  # if we got to the last page, the update is valid
                break
            if page not in rules[:, 1]:
                continue
            idx = np.where(rules[:, 1] == page)[0]
            for rule in rules[idx, 0]:
                if rule in update[k + 1 :]:
                    valid = False
                    break
            if not valid:
                invalids.append(update)
                break
    return invalids


def build_graph(rules: NDArray[np.int8]) -> nx.DiGraph:
    """Create a directed graph from the rule set."""
    G = nx.DiGraph()
    # add edges from the rules, each rule is of the form X|Y, meaning X -> Y
    for X, Y in rules:
        G.add_edge(X, Y)
    return G


def reorder_updates(updates: list[list[int]], ruleset: nx.DigGraph) -> list[list[int]]:
    """Reorder the update using the ruleset."""
    valid_updates = []
    for update in updates:
        subG = ruleset.subgraph(update)
        valid_updates.append(np.array(list(nx.topological_sort(subG)), dtype=np.int8))
    return [update.tolist() for update in valid_updates]  # cast back to list


def get_middle_page_sum(updates: list[list[int]]) -> int:
    """Get the middle page of an update."""
    count = 0
    for update in updates:
        count += update[len(update) // 2]
    return count


invalids = get_updates_incorrectly_ordered(updates, rules)
ruleset = build_graph(rules)
valid_updates = reorder_updates(invalids, ruleset)
total = get_middle_page_sum(valid_updates)
print(f"The sum of the middle pages is {total}.")
