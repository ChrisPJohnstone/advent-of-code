#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from functools import cache
import logging


def read_input(filepath: str) -> list[int]:
    with open(filepath, "r") as file:
        return [int(stone) for stone in file.read().split(" ")]


@cache
def blink(stone: int, n: int) -> int:
    if n == 0:
        return 1
    recurse: Callable = lambda x: blink(x, n - 1)
    if stone == 0:
        return recurse(1)
    length: int = len(str(stone))
    if length % 2 == 0:
        left: int = int(str(stone)[: length // 2])
        right: int = int(str(stone)[length // 2 :])
        return recurse(left) + recurse(right)
    return recurse(stone * 2024)



def main(input_path: str, blinks: int) -> int:
    stones: list[int] = read_input(input_path)
    output: int = 0
    for n, stone in enumerate(stones):
        logging.debug(f"Starting stone {n} value {stone}")
        output += blink(stone, blinks)
    return output


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument(dest="blinks", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    stones: int = main(args.path[0], int(args.blinks[0]))
    print(f"Stones: {stones}")
