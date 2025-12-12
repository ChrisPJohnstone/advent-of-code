#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from re import findall

PATTERN: str = r"mul\((\d{1,3}),(\d{1,3})\)"


def read_data(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()


def main(input_path: str) -> int:
    total: int = 0
    instruction_set: str = read_data(input_path)
    instructions: list[str] = findall(PATTERN, instruction_set)
    for instruction in instructions:
        total += int(instruction[0]) * int(instruction[1])
    return total


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    args: Namespace = parser.parse_args()
    total: int = main(args.path[0])
    print(f"The total is {total}")
