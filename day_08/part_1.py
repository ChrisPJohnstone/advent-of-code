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


def is_antinode(
    antenna_1: Position,
    antenna_2: Position,
    position: Position,
    max_x: int,
    max_y: int,
) -> bool:
    if is_out_of_bounds(position, max_x, max_y):
        return False
    antenna_1_diff_x: int = abs(antenna_1[0] - position[0])
    antenna_2_diff_x: int = abs(antenna_2[0] - position[0])
    min_diff_x: int = min(antenna_1_diff_x, antenna_2_diff_x)
    if antenna_1_diff_x + antenna_2_diff_x != min_diff_x * 3:
        return False
    antenna_1_diff_y: int = abs(antenna_1[1] - position[1])
    antenna_2_diff_y: int = abs(antenna_2[1] - position[1])
    min_diff_y: int = min(antenna_1_diff_y, antenna_2_diff_y)
    if antenna_1_diff_y + antenna_2_diff_y != min_diff_y * 3:
        return False
    return True


def _find_antinodes(
    antenna_1: Position,
    antenna_2: Position,
    max_x: int,
    max_y: int,
) -> set[Position]:
    a_x: int = antenna_1[0]
    a_y: int = antenna_1[1]
    b_x: int = antenna_2[0]
    b_y: int = antenna_2[1]
    diff_x: int = abs(a_x - b_x)
    diff_y: int = abs(a_y - b_y)
    if a_x < b_x:
        next_x_1: int = a_x - diff_x
        next_x_2: int = b_x + diff_x
    else:
        next_x_1: int = a_x + diff_x
        next_x_2: int = b_x - diff_x
    if a_y < b_y:
        next_y_1: int = a_y - diff_y
        next_y_2: int = b_y + diff_y
    else:
        next_y_1: int = a_y + diff_y
        next_y_2: int = b_y - diff_y
    possible_positions: set[Position] = {
        (next_x_1, next_y_1),
        (next_x_2, next_y_2),
    }
    antinodes: set[Position] = set()
    for position in possible_positions:
        if is_antinode(antenna_1, antenna_2, position, max_x, max_y):
            logging.debug(f"Antinode: {position}")
            antinodes.add(position)
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
