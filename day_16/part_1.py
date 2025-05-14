#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections import deque
from collections.abc import Callable, Iterator
import logging

type XY = tuple[int, int]
type Maze = list[list[str | int]]

START_CHAR: str = "S"
END_CHAR: str = "E"
SPACE_CHAR: str = "."
WALL_CHAR: str = "#"
START_DIRECTION: int = 1
DIRECTIONS: list[Callable[[int, int], XY]] = [
    lambda x, y: (x, y - 1),  # N
    lambda x, y: (x + 1, y),  # E
    lambda x, y: (x, y + 1),  # S
    lambda x, y: (x - 1, y),  # W
]


def read_input(filepath: str) -> Maze:
    with open(filepath, "r") as file:
        lines: list[str] = file.read().splitlines()
    return [list(line) for line in lines]


def start(maze: Maze) -> XY:
    output: XY = (-1, -1)
    for y, line in enumerate(maze):
        if START_CHAR in line:
            output: XY = (line.index(START_CHAR), y)
    if output == (-1, -1):
        raise ValueError(f"Start character '{START_CHAR}' not found in maze.")
    return output


def moves(direction: int, score: int) -> Iterator[tuple[int, int]]:
    yield direction, score + 1
    yield (direction + 1) % len(DIRECTIONS), score + 1001
    yield (direction + 3) % len(DIRECTIONS), score + 1001


def lowest_score(maze: Maze) -> int:
    queue: deque = deque()
    _start: XY = start(maze)
    queue.append((*_start, START_DIRECTION, 0))  # (x, y, direction, score)
    maze[_start[1]][_start[0]] = WALL_CHAR
    while queue:
        x, y, direction, score = queue.popleft()
        position: XY = (x, y)
        for new_direction, new_score in moves(direction, score):
            new_position: XY = DIRECTIONS[new_direction](*position)
            new_x: int = new_position[0]
            new_y: int = new_position[1]
            new: str | int = maze[new_y][new_x]
            is_new_int: bool = isinstance(new, int)
            if new == WALL_CHAR:
                continue
            if new not in [SPACE_CHAR, END_CHAR] and not is_new_int:
                continue
            if is_new_int and new <= new_score:
                continue
            maze[new_y][new_x] = new_score
            queue.append((*new_position, new_direction, new_score))
    return int(maze[1][len(maze[1]) - 2])


def main(input_path: str) -> int:
    maze: Maze = read_input(input_path)
    return lowest_score(maze)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    output: int = main(args.path[0])
    print(f"The lowest score is: {output}")
