from __future__ import annotations

from pathlib import Path

fname: Path = Path(__file__).parent / "input.txt"
with open(fname) as fid:
    lines: list[str] = [elt.strip().split(" ") for elt in fid.readlines()]
MAP_SIZE: tuple[int, int] = (11, 7) if fname.name == "example.txt" else (101, 103)
# /!\ does not respect the numpy convention.


# %% part 1
class Robot:
    """Object representing a robot with its 2D position and velocity."""

    def __init__(self, x: int, y: int, vx: int, vy: int) -> None:
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy

    def move(self) -> None:
        """Move the robot during 1 second."""
        new_x = self._x + self._vx
        if 0 <= new_x:
            self._x = new_x % MAP_SIZE[0]
        else:
            self._x = MAP_SIZE[0] + new_x
        new_y = self._y + self._vy
        if 0 <= new_y:
            self._y = new_y % MAP_SIZE[1]
        else:
            self._y = MAP_SIZE[1] + new_y

    def __repr__(self) -> str:
        """Representation of the robot."""
        return f"<Robot @ ({self._x}, {self._y}) moving @ ({self._vx}, {self._vy})>"

    @property
    def quadrant(self) -> int | None:
        """Quandrant in which the robot is, or None if it's in-between."""
        if 0 <= self._x < MAP_SIZE[0] // 2 and 0 <= self._y < MAP_SIZE[1] // 2:
            return 0  # top-left
        elif 0 <= self._x < MAP_SIZE[0] // 2 and MAP_SIZE[1] // 2 < self._y:
            return 1  # bottom-left
        elif MAP_SIZE[0] // 2 < self._x and 0 <= self._y < MAP_SIZE[1] // 2:
            return 2  # top-right
        elif MAP_SIZE[0] // 2 < self._x and MAP_SIZE[1] // 2 < self._y:
            return 3  # bottom-right
        else:
            return None


def list_robots(lines: list[str]) -> list[Robot]:
    """Parse the input in a list of robots."""
    robots = []
    for line in lines:
        x, y = map(int, line[0].split("=")[1].split(","))
        vx, vy = map(int, line[1].split("=")[1].split(","))
        robots.append(Robot(x, y, vx, vy))
    return robots


def move_robots(robots: list[Robot], n: int) -> None:
    """Move the robots during n seconds."""
    for k, robot in enumerate(robots):
        print(f"Moving robot {k+1} / {len(robots)}.")
        for _ in range(n):
            robot.move()


def compute_safety_factor(robots: list[Robot]):
    """Count the robots in the 4 quadrant."""
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        quad = robot.quadrant
        if quad is not None:
            quadrants[quad] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


robots = list_robots(lines)
move_robots(robots, 100)
safety_factor = compute_safety_factor(robots)
print(f"The safety factor is {safety_factor}.")
