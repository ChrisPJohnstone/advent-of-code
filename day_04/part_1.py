#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable

WORD: str = "XMAS"
DIRECTIONS: dict[str, Callable] = {
    "N": lambda x, y, n: (x, y - n),
    "NE": lambda x, y, n: (x + n, y - n),
    "E": lambda x, y, n: (x + n, y),
    "SE": lambda x, y, n: (x + n, y + n),
    "S": lambda x, y, n: (x, y + n),
    "SW": lambda x, y, n: (x - n, y + n),
    "W": lambda x, y, n: (x - n, y),
    "NW": lambda x, y, n: (x - n, y - n),
}


def read_input(filepath: str) -> list[list[str]]:
    with open(filepath, "r") as file:
        return [list(line[:-1]) for line in file.readlines()]


def is_match(grid: list[list[str]], direction: str, x: int, y: int) -> bool:
    for n in range(1, len(WORD)):
        next_x, next_y = DIRECTIONS[direction](x, y, n)
        if 0 > next_x or next_x >= len(grid[0]):
            return False
        if 0 > next_y or next_y >= len(grid):
            return False
        next_char: str = grid[next_y][next_x]
        if next_char != WORD[n]:
            return False
    return True


def count_matches(grid: list[list[str]], x: int, y: int) -> int:
    directions: dict[str, int] = {
        direction: is_match(grid, direction, x, y)
        for direction in DIRECTIONS.keys()
    }
    return sum(directions.values())


def main(input_path: str) -> int:
    counter: int = 0
    grid: list[list[str]] = read_input(input_path)
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char != "X":
                continue
            counter += count_matches(grid, x, y)
    return counter


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    args: Namespace = parser.parse_args()
    matches: int = main(args.path[0])
    print(f"There are {matches} matches")
