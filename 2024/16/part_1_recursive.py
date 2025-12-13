#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Iterator
import logging

type XY = tuple[int, int]
type Direction = Callable[[int, int], XY]

START_CHAR: str = "S"
END_CHAR: str = "E"
WALL_CHAR: str = "#"
START_DIRECTION: int = 1
DIRECTIONS: list[Direction] = [
    lambda x, y: (x, y - 1),  # N
    lambda x, y: (x + 1, y),  # E
    lambda x, y: (x, y + 1),  # S
    lambda x, y: (x - 1, y),  # W
]


def read_input(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()


def char_position(position: int, width: int) -> XY:
    x: int = position % width
    y: int = position // width
    return x, y


def maze_spaces(maze: str) -> set[XY]:
    output: set[XY] = set()
    for y, line in enumerate(maze.splitlines()):
        for x, char in enumerate(line):
            if char == WALL_CHAR:
                continue
            output.add((x, y))
    return output


def route_scores(
    position: XY,
    end: XY,
    spaces: set[XY],
    spaces_visited: set[XY] = set(),
    direction: int = START_DIRECTION,
    steps: int = 0,
    turns: int = 0,
) -> Iterator[int]:
    if position == end:
        score: int = steps + (turns * 1000)
        logging.debug(f"Steps {steps:3d}. Turns {turns:3d}. Score {score}")
        yield score
    n_directions: int = len(DIRECTIONS)
    for n in range(direction, direction + 4):
        new_direction: int = n % n_directions
        if abs(direction - new_direction) == 2:
            continue
        new: XY = DIRECTIONS[new_direction](*position)
        if new not in spaces:
            continue
        if new in spaces_visited:
            continue
        new_spaces_visited: set[XY] = spaces_visited.copy()
        new_spaces_visited.add(new)
        yield from route_scores(
            position=new,
            end=end,
            spaces=spaces,
            spaces_visited=new_spaces_visited,
            direction=new_direction,
            steps=steps + 1,
            turns=turns + (n - direction) % 2,
        )


def main(input_path: str) -> int:
    maze: str = read_input(input_path)
    width: int = maze.find("\n")
    start: XY = char_position(maze.replace("\n", "").find(START_CHAR), width)
    end: XY = char_position(maze.replace("\n", "").find(END_CHAR), width)
    logging.debug(f"Start {start}. End {end}")
    spaces: set[XY] = maze_spaces(maze)
    return min(list(route_scores(start, end, spaces)))


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    output: int = main(args.path[0])
    print(f"The sum of coordinates is: {output}")
