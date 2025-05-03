#!/usr/bin/env python
from argparse import ArgumentParser, Namespace


def read_input(filepath: str) -> tuple[list[int]]:
    left: list[int] = []
    right: list[int] = []
    with open(filepath, "r") as file:
        for line in file:
            left.append(int(line[: line.find(" ")]))
            right.append(int(line[-line[::-1].find(" ") : -1]))
    return left, right


def main(input_path: str) -> int:
    left, right = read_input(input_path)
    similarity: int = 0
    for location in left:
        similarity += location * right.count(location)
    return similarity


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    args: Namespace = parser.parse_args()
    similarity: int = main(args.path[0])
    print(f"The similarity score is {similarity}")
