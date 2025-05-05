#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Iterator
from itertools import cycle
import logging


class Patrol:
    DIRECTIONS: list[Callable] = [
        lambda x, y: (x, y - 1),
        lambda x, y: (x + 1, y),
        lambda x, y: (x, y + 1),
        lambda x, y: (x - 1, y),
    ]

    def __init__(
        self,
        start_x: int,
        start_y: int,
        max_x: int,
        max_y: int,
        obstacles: set[tuple[int, int]],
    ) -> None:
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.max_x: int = max_x
        self.max_y: int = max_y
        self.obstacles: set[tuple[int, int]] = obstacles
        self.reset()

    @property
    def position(self) -> tuple[int, int, Callable]:
        return (self.x, self.y, self.direction)

    @property
    def is_in_bounds(self) -> bool:
        if 0 > self.x or self.x > self.max_x:
            return False
        if 0 > self.y or self.y > self.max_y:
            return False
        return True

    def reset(self) -> None:
        self.x: int = self.start_x
        self.y: int = self.start_y
        self.directions: Iterator[Callable] = cycle(self.DIRECTIONS)
        self.direction: Callable = next(self.directions)
        self.visited: set[tuple[int, int, Callable]] = {self.position}

    def turn(self) -> None:
        logging.debug("Changing directions")
        self.direction: Callable = next(self.directions)

    def move(self) -> bool:
        next_x, next_y = self.direction(self.x, self.y)
        logging.info(f"Moving from ({self.x},{self.y}) to ({next_x},{next_y})")
        if (next_x, next_y) in self.obstacles:
            logging.debug(
                f"Obstacle encountered at ({next_x},{next_y}) "
                f"from ({self.x},{self.y})"
            )
            self.turn()
            return self.move()
        self.x: int = next_x
        self.y: int = next_y
        if self.position not in self.visited:
            self.visited.add(self.position)
            return False
        return True


def read_input(filepath: str) -> Patrol:
    with open(filepath, "r") as file:
        lines: list[str] = file.readlines()
    start_position: tuple[int, int] = ()
    obstacles: set[tuple[int, int]] = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line[:-1]):
            if char == ".":
                continue
            if char == "^":
                start_position: tuple[int, int] = (x, y)
                continue
            if char == "#":
                obstacles.add((x, y))
                continue
            raise ValueError(f"Unknown char {char} at ({x}, {y})")
    if not start_position:
        raise ValueError("Start position not found")
    return Patrol(
        start_x=start_position[0],
        start_y=start_position[1],
        max_x=len(lines[0][:-1]) - 1,
        max_y=len(lines) - 1,
        obstacles=obstacles,
    )


def is_looping_patrol(patrol: Patrol, new_obstacle: tuple[int, int]) -> bool:
    if new_obstacle in patrol.obstacles:
        return False
    logging.debug(f"Checking {new_obstacle}")
    patrol.obstacles.add(new_obstacle)
    is_looping: bool = False
    while patrol.is_in_bounds and not is_looping:
        is_looping: bool = patrol.move()
    patrol.obstacles.discard(new_obstacle)
    patrol.reset()
    return is_looping


def main(input_path: str) -> int:
    patrol: Patrol = read_input(input_path)
    counter: int = 0
    for x in range(patrol.max_x + 1):
        for y in range(patrol.max_y + 1):
            counter += int(is_looping_patrol(patrol, (x, y)))
    return counter


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    patrols: int = main(args.path[0])
    print(f"There are {patrols} possible looping patrols")
