#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Iterator
from itertools import cycle


class Patrol:
    DIRECTIONS: Iterator[Callable] = cycle(
        [
            lambda coordinates: (coordinates[0], coordinates[1] - 1),
            lambda coordinates: (coordinates[0] + 1, coordinates[1]),
            lambda coordinates: (coordinates[0], coordinates[1] + 1),
            lambda coordinates: (coordinates[0] - 1, coordinates[1]),
        ]
    )

    def __init__(
        self,
        start_x: int,
        start_y: int,
        max_x: int,
        max_y: int,
        obstacles: set[tuple[int, int]],
    ) -> None:
        self.turn()
        self.x: int = start_x
        self.y: int = start_y
        self.max_x: int = max_x
        self.max_y: int = max_y
        self.obstacles: set[tuple[int, int]] = obstacles
        self.visited: set[tuple[int, int]] = {self.position}

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def turn(self) -> None:
        self.direction: Callable = next(self.DIRECTIONS)

    def move(self) -> bool:
        next_x, next_y = self.direction(self.position)
        if 0 > next_x or next_x > self.max_x:
            return False
        if 0 > next_y or next_y > self.max_y:
            return False
        if (next_x, next_y) in self.obstacles:
            self.turn()
            return self.move()
        self.x: int = next_x
        self.y: int = next_y
        if self.position not in self.visited:
            self.visited.add(self.position)
        return True


def read_input(filepath: str) -> Patrol:
    with open(filepath, "r") as file:
        lines: list[str] = file.readlines()
    start_position: tuple[int, int] = (0, 0)
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
    if start_position == (0, 0):
        raise ValueError("Start position not found")
    return Patrol(
        start_x=start_position[0],
        start_y=start_position[1],
        max_x=len(lines[0][:-1]) - 1,
        max_y=len(lines) - 1,
        obstacles=obstacles,
    )


def main(input_path: str) -> int:
    is_in_bounds: bool = True
    patrol: Patrol = read_input(input_path)
    while is_in_bounds:
        is_in_bounds: bool = patrol.move()
    return len(patrol.visited)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    args: Namespace = parser.parse_args()
    distance: int = main(args.path[0])
    print(f"The patrole length is {distance}")
