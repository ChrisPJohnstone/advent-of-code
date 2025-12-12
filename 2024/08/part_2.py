#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from itertools import combinations
import logging

type Position = tuple[int, int]
type Antennas = dict[str, set[Position]]


def read_input(filepath: str) -> tuple[int, int, Antennas]:
    with open(filepath, "r") as file:
        lines: list[str] = file.read().splitlines()
    output: defaultdict = defaultdict(set)
    max_x: int = len(lines[0])
    max_y: int = len(lines)
    for y in range(max_y):
        for x in range(max_x):
            char: str = lines[y][x]
            if char == ".":
                continue
            output[char].add((x, y))
    return max_x, max_y, dict(output)


def is_out_of_bounds(position: Position, max_x: int, max_y: int) -> bool:
    if position[0] < 0 or position[0] >= max_x:
        return True
    if position[1] < 0 or position[1] >= max_y:
        return True
    return False


def _find_antinodes(
    antenna_1: Position,
    antenna_2: Position,
    max_x: int,
    max_y: int,
) -> set[Position]:
    diff_x: int = antenna_1[0] - antenna_2[0]
    diff_y: int = antenna_1[1] - antenna_2[1]
    antinodes: set[Position] = set()
    current_position: Position = antenna_1
    while not is_out_of_bounds(current_position, max_x, max_y):
        logging.debug(f"Antinode: {current_position}")
        antinodes.add(current_position)
        current_position = (
            current_position[0] + diff_x,
            current_position[1] + diff_y,
        )
    logging.debug(f"Switching direction")
    current_position: Position = antenna_1
    while not is_out_of_bounds(current_position, max_x, max_y):
        logging.debug(f"Antinode: {current_position}")
        antinodes.add(current_position)
        current_position = (
            current_position[0] - diff_x,
            current_position[1] - diff_y,
        )
    return antinodes


def find_antinodes(
    antennas: set[Position],
    max_x: int,
    max_y: int,
) -> set[Position]:
    antinodes: set[Position] = set()
    for combination in combinations(antennas, 2):
        logging.debug(f"Combination: {combination}")
        antinodes.update(_find_antinodes(*combination, max_x, max_y))
    return antinodes


def main(input_path: str) -> int:
    all_input: tuple[int, int, Antennas] = read_input(input_path)
    antinodes: set[Position] = set()
    for antennas in all_input[2].values():
        if len(antennas) < 2:
            continue
        logging.debug(f"Positions: {antennas}")
        antinodes.update(find_antinodes(antennas, all_input[0], all_input[1]))
    logging.debug(f"Antinodes: {antinodes}")
    return len(antinodes)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    safe: int = main(args.path[0])
    print(f"The number of safe reports is: {safe}")
