#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Iterator
import logging

type TopographicMap = list[list[int]]
type Position = tuple[int, int]


DIRECTIONS: list[Callable] = [
    lambda x, y: (x, y - 1),  # Up
    lambda x, y: (x, y + 1),  # Down
    lambda x, y: (x - 1, y),  # Left
    lambda x, y: (x + 1, y),  # Right
]


def read_input(filepath: str) -> TopographicMap:
    with open(filepath, "r") as file:
        lines: list[str] = file.read().splitlines()
    return [[int(n) for n in list(line)] for line in lines]


def is_in_bounds(x: int, y: int, width: int, height: int) -> bool:
    if x < 0 or y < 0:
        return False
    if x >= width or y >= height:
        return False
    return True


def _trails(
    topographic_map: TopographicMap,
    start: Position,
    width: int,
    height: int,
) -> Iterator[Position]:
    cur_x: int = start[0]
    cur_y: int = start[1]
    cur_height: int = topographic_map[cur_y][cur_x]
    for direction in DIRECTIONS:
        new_position: Position = direction(cur_x, cur_y)
        new_x: int = new_position[0]
        new_y: int = new_position[1]
        if not is_in_bounds(new_x, new_y, width, height):
            continue
        new_height: int = topographic_map[new_y][new_x]
        if new_height != cur_height + 1:
            continue
        if new_height == 9:
            logging.debug(f"Found a trail at {new_x}, {new_y}")
            yield new_position
        for trail in _trails(topographic_map, (new_x, new_y), width, height):
            yield trail


def trails(topographic_map: TopographicMap) -> int:
    width: int = len(topographic_map[0])
    height: int = len(topographic_map)
    trails: set[str] = set()
    for y in range(height):
        logging.debug(f"Starting Row {topographic_map[y]}")
        for x in range(width):
            cur_height: int = topographic_map[y][x]
            if cur_height != 0:
                continue
            start_position: Position = (x, y)
            logging.debug(f"Checking start position at {start_position}")
            for trail in _trails(topographic_map, (x, y), width, height):
                trails.add(f"{start_position}:{trail}")
    logging.debug(f"Found trails: {trails}")
    return len(trails)


def main(input_path: str) -> int:
    topographic_map: TopographicMap = read_input(input_path)
    return trails(topographic_map)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    valid_trails: int = main(args.path[0])
    print(f"Number of valid trails: {valid_trails}")
