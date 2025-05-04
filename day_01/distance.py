#!/usr/bin/env python
from argparse import ArgumentParser, Namespace


def read_input(filepath: str) -> tuple[list[int]]:
    left: list[int] = []
    right: list[int] = []
    with open(filepath, "r") as file:
        for line in file:
            nums: list[str] = line.split(" ")
            left.append(int(nums[0]))
            right.append(int(nums[-1][:-1]))
    left.sort()
    right.sort()
    return left, right


def main(input_path: str) -> int:
    left, right = read_input(input_path)
    distance: int = 0
    for n in range(len(left)):
        distance += abs(left[n] - right[n])
    return distance


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    args: Namespace = parser.parse_args()
    distance: int = main(args.path[0])
    print(f"The total distance is {distance}")
