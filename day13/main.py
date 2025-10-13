from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from sympy import Matrix, symbols

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    lines: list[str] = fid.readlines()
lines: list[tuple[str, str, str]] = list(
    zip(lines[::4], lines[1::4], lines[2::4], strict=False)
)
data: list[dict[str, NDArray[np.int64]]] = []
pattern = re.compile(r"(\d+)")
for line in lines:
    data_ = dict()
    for elt, line_ in zip(("A", "B", "Prize"), line, strict=True):
        x, y = re.findall(pattern, line_)
        data_[elt] = np.array((int(x), int(y)), dtype=int)
    data.append(data_)


# %% part 1
def solve_machine(data: dict[str, NDArray[np.int64]]) -> list[tuple[int, int]]:
    """Solve a given machine problem."""
    A, B, Prize = data["A"], data["B"], data["Prize"]
    solutions = []
    for a in range(101):
        b = (Prize[0] - a * A[0]) / B[0]
        if b.is_integer() and 0 <= b <= 100 and a * A[1] + b * B[1] == Prize[1]:
            solutions.append((a, int(b)))
    return solutions


def compute_solution_cost(solution) -> int:
    """Compute the cost of a solution."""
    return 3 * solution[0] + solution[1]


def resolve(data: list[dict[str, NDArray[np.int64]]]) -> int:
    """Solve all machine claw problems."""
    total = 0
    for data_ in data:
        solutions = solve_machine(data_)
        if len(solutions) == 0:
            continue
        costs = [compute_solution_cost(solution) for solution in solutions]
        total += min(costs)
    return total


total = resolve(data)
print(f"The minimum number of token to spend is {total}.")


# %% part 2
def solve_diophantine_system(A_x, A_y, B_x, B_y, P_x, P_y) -> tuple[int, int] | None:
    """Solve the system of diophantine linear equations."""
    a, b = symbols("a b", integer=True)
    # represent the system in matrix form for analysis
    M = Matrix([[A_x, B_x], [A_y, B_y]])
    rhs = Matrix([P_x, P_y])
    det = M.det()
    if det == 0:
        # theoretically, a solution might exist along a line of infinite solutions if
        # the 2 equations are linearly dependent but this is not the case with the
        # input data given.
        print("The system is singular.")
        return None
    else:
        a_sol, b_sol = M.LUsolve(rhs)  # returns rational solutions for a, b
        if a_sol.is_integer and b_sol.is_integer:
            return a_sol, b_sol


def resolve(data: list[dict[str, NDArray[np.int64]]]) -> int:  # noqa: F811
    """Solve all machine claw problems."""
    total = 0
    for data_ in data:
        data_["Prize"] += 10000000000000
        solution = solve_diophantine_system(*data_["A"], *data_["B"], *data_["Prize"])
        if solution is None:
            continue
        total += compute_solution_cost(solution)
    return total


total = resolve(data)
print(f"The minimum number of token to spend is {total}.")
