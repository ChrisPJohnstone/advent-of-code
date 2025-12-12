#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from re import Match, search

DO_PATTERN: str = r"do\(\)"
DONT_PATTERN: str = r"don't\(\)"
MUL_PATTERN: str = r"mul\((\d{1,3}),(\d{1,3})\)"


def read_data(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()


def read_instructions(
    instructions: str,
    enabled: bool = True,
    total: int = 0,
) -> int:
    if not enabled:
        next_do: Match | None = search(DO_PATTERN, instructions)
        if next_do is None:
            return total
        return read_instructions(instructions[next_do.end() :], total=total)
    next_mul: Match | None = search(MUL_PATTERN, instructions)
    if next_mul is None:
        return total
    next_dont: Match | None = search(DONT_PATTERN, instructions)
    if next_dont is not None and next_dont.start() < next_mul.start():
        return read_instructions(
            instructions[next_dont.end() :],
            enabled=False,
            total=total,
        )
    total += int(next_mul[1]) * int(next_mul[2])
    return read_instructions(instructions[next_mul.end() :], total=total)


def main(input_path: str) -> int:
    instructions: str = read_data(input_path)[:-1]
    return read_instructions(instructions)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    args: Namespace = parser.parse_args()
    total: int = main(args.path[0])
    print(f"The total is {total}")
