from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    text: list[str] = fid.read().split("\n")
split_idx: int = text.index("")
char_to_num: dict[str, int] = {".": 0, "#": 1, "O": 2, "@": 3}
data: list[int] = [[char_to_num[char] for char in line] for line in text[:split_idx]]
data: NDArray[np.int8] = np.array(data, dtype=np.int8)
instructions: list[str] = [elt for elt in text[split_idx + 1 :] if len(elt) != 0]
instructions: str = "".join(instructions)
# extract the robot position
x, y = np.where(data == 3)
x, y = x[0], y[0]
data[x, y] = 0


# %% part 1
_DIRECTIONS: dict[str, NDArray[np.int8]] = {
    ">": np.array([0, 1], dtype=np.int8),
    "<": np.array([0, -1], dtype=np.int8),
    "^": np.array([-1, 0], dtype=np.int8),
    "v": np.array([1, 0], dtype=np.int8),
}


class AutomaticWarehouseSystem:
    """An object representing the warehouse and the robot."""

    def __init__(self, warehouse: NDArray[np.int8], robot_x: int, robot_y: int) -> None:
        self._map = warehouse
        self._robot = np.array([robot_x, robot_y], dtype=np.int8)

    def move(self, direction: str) -> None:
        """Attempt to move the robot in the direction."""
        direction = _DIRECTIONS[direction]
        new_pos = self._robot + direction
        if self._map[*new_pos] == 0:
            self._robot = new_pos
            return
        elif self._map[*new_pos] == 1:
            return
        elif self._map[*new_pos] == 2:
            temp_pos = new_pos.copy()
            while True:
                temp_pos += direction
                if self._map[*temp_pos] == 2:
                    continue
                elif self._map[*temp_pos] == 0:
                    self._map[*temp_pos], self._map[*new_pos] = (
                        self._map[*new_pos],
                        self._map[*temp_pos],
                    )
                    self._robot = new_pos
                    break
                elif self._map[*temp_pos] == 1:
                    break
        else:
            raise RuntimeError("Invalid map position/value.")


def simulate(warehouse: AutomaticWarehouseSystem, instructions: str) -> None:
    """Simulate the set of instruction for the given warehouse."""
    for direction in instructions:
        warehouse.move(direction)


def sum_gps_coordinates(warehouse: AutomaticWarehouseSystem) -> int:
    """Sum the gps coordinates of box in the warehouse."""
    pos = np.where(warehouse._map == 2)
    return np.sum(100 * pos[0] + pos[1])


warehouse = AutomaticWarehouseSystem(data, x, y)
simulate(warehouse, instructions)
total = sum_gps_coordinates(warehouse)
print(f"The sum of the box GPS coordinates is {total}.")

# %% part 2
