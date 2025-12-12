#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
import logging


def read_input(filepath: str) -> list[int]:
    with open(filepath, "r") as file:
        return [int(stone) for stone in file.read().split(" ")]


def _blink(stone: int) -> list[int]:
    if stone == 0:
        logging.debug("{stone} = 0. Returning 1")
        return [1]
    length: int = len(str(stone))
    if length % 2 == 0:
        left: int = int(str(stone)[: length // 2])
        right: int = int(str(stone)[length // 2 :])
        logging.debug(f"{stone} even length. Returning {left} and {right}")
        return [left, right]
    new: int = stone * 2024
    logging.debug(f"{stone} meets no rules. Returning {new}")
    return [new]


def blink(stones: list[int]) -> list[int]:
    output: list[int] = []
    for stone in stones:
        new: list[int] = _blink(stone)
        output.extend(new)
    return output


def main(input_path: str, blinks: int) -> int:
    stones: list[int] = read_input(input_path)
    for n in range(blinks):
        logging.debug(f"Blink {n}: {stones}")
        stones: list[int] = blink(stones)
    return len(stones)


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
