from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    data: list[str] = fid.readlines()

# split the input between the page ordering rules and the updates.
split: int = data.index("\n")
rules: list[list[int]] = [
    [int(page) for page in elt.strip().split("|")] for elt in data[:split]
]
updates: list[list[int]] = [
    [int(page) for page in elt.strip().split(",")] for elt in data[split + 1 :]
]

G_rules = nx.DiGraph()
# add edges from the rules, each rule is of the form X|Y, meaning X -> Y
for X, Y in rules:
    G_rules.add_edge(X, Y)


# %% part 1
def is_valid(update: list[int], G_ruleset: nx.DiGraph) -> bool:
    """Check if an update is valid."""
    G_sub = G_ruleset.subgraph(update)
    position = {page: i for i, page in enumerate(update)}
    # check all edges in the subgraph
    for X, Y in G_sub.edges():
        # if X must come before Y, but X's position is not before Y's, it's invalid
        if position[Y] <= position[X]:
            return False
    return True  # if no edges are violated, the update is valid


def find_middle_page_of_valid_updates(
    updates: list[list[int]], G_ruleset: nx.DiGraph
) -> list[int]:
    """Find the middle page of the valid updates."""
    middle_pages = []
    for update in updates:
        if is_valid(update, G_ruleset):
            middle_pages.append(update[len(update) // 2])
    return middle_pages


middle_pages = find_middle_page_of_valid_updates(updates, G_rules)
print(f"The sum of the middle pages is {np.sum(middle_pages)}.")


# %% part 2
def find_invalid_updates(
    updates: list[list[int]], G_ruleset: nx.DiGraph
) -> list[list[int]]:
    """Find the incorrectly ordered updates."""
    invalids = []
    for update in updates:
        if not is_valid(update, G_ruleset):
            invalids.append(update)
    return invalids


def reorder_updates(
    updates: list[list[int]], G_ruleset: nx.DigGraph
) -> list[list[int]]:
    """Reorder the update using the ruleset."""
    valid_updates = []
    for update in updates:
        G_sub = G_ruleset.subgraph(update)
        valid_updates.append(np.array(list(nx.topological_sort(G_sub)), dtype=np.int8))
    return [update.tolist() for update in valid_updates]  # cast back to list


def get_middle_page_sum(updates: list[list[int]]) -> int:
    """Get the middle page of an update."""
    count = 0
    for update in updates:
        count += update[len(update) // 2]
    return count


invalids = find_invalid_updates(updates, G_rules)
valid_updates = reorder_updates(invalids, G_rules)
total = get_middle_page_sum(valid_updates)
print(f"The sum of the middle pages is {total}.")
