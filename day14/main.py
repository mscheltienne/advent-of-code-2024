from __future__ import annotations

from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

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

    @property
    def x(self) -> int:
        """The X-position of the robot."""
        return self._x

    @property
    def y(self) -> int:
        """The Y-position of the robot."""
        return self._y

    @property
    def vx(self) -> int:
        """The X-velocity of the robot."""
        return self._vx

    @property
    def vy(self) -> int:
        """The Y-velocity of the robot."""
        return self._vy


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


def compute_safety_factor(robots: list[Robot]) -> int:
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


# %% part 2
def plot_map(robots: list[Robot], t_start: int = 0) -> None:
    """Plot an interactive map of the robot positions."""
    if plt.get_backend() != "QtAgg":
        plt.switch_backend("QtAgg")
    if not plt.isinteractive():
        plt.ion()
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.set_xlim(0, MAP_SIZE[0])
    ax.set_ylim(0, MAP_SIZE[1])
    ax.set_aspect("equal")
    ax.set_title("Press Space to step forward 1 second")

    for _ in range(t_start):
        for r in robots:
            r.move()

    scatter = ax.scatter([r.x for r in robots], [r.y for r in robots], c="r", s=10)
    time_step = t_start

    def update_plot() -> None:
        """Udpdate the positions on the plot."""
        scatter.set_offsets([[r.x, r.y] for r in robots])
        ax.set_title(f"Time: {time_step} seconds (press Space to step)")
        fig.canvas.draw_idle()

    def on_key(event) -> None:
        nonlocal time_step
        # Step forward one second if user presses space
        if event.key == " ":
            time_step += 1
            for r in robots:
                r.move()
            update_plot()

    # Connect the event
    fig.canvas.mpl_connect("key_press_event", on_key)
    update_plot()
    plt.show(block=True)


def compute_variance(robots: list[Robot]) -> float:
    """Compute the X/Y variance of the robot distribution."""
    xs = np.array([r.x for r in robots])
    ys = np.array([r.y for r in robots])
    xvar = np.var(xs)
    yvar = np.var(ys)
    return xvar + yvar


def find_xmas_tree(robots: list[Robot], n_iter: int) -> int:
    """Find the position which minimizes the entropy of the robot-point-cloud."""
    pos = None
    min_var = None
    for k in range(n_iter):
        var = compute_variance(robots)
        if min_var is None or var < min_var:
            min_var = var
            pos = k
        for robot in robots:
            robot.move()
    return pos


robots = list_robots(lines)
pos = find_xmas_tree(robots, 10000)
robots = list_robots(lines)
print(f"The timestamp forming a X-mas tree is {pos}.")
plot_map(robots, pos)
