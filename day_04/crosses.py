#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable

WORD: str = "MAS"


def read_input(filepath: str) -> str:
    with open(filepath, "r") as file:
        return [list(line[:-1]) for line in file.readlines()]


def is_match(grid: list[str], x: int, y: int) -> bool:
    diagonal_1: list[str] = [grid[y - 1][x - 1], grid[y][x], grid[y + 1][x + 1]]
    if "".join(diagonal_1) not in [WORD, WORD[::-1]]:
        return False
    diagonal_2: list[str] = [grid[y - 1][x + 1], grid[y][x], grid[y + 1][x - 1]]
    if "".join(diagonal_2) not in [WORD, WORD[::-1]]:
        return False
    return True


def main(input_path: str) -> int:
    counter: int = 0
    grid: list[str] = read_input(input_path)
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] != "A":
                continue
            counter += int(is_match(grid, x, y))
    return counter


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    args: Namespace = parser.parse_args()
    matches: int = main(args.path[0])
    print(f"There are {matches} matches")
