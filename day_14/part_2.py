#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Iterator
from re import Match, match
import logging

type XY = tuple[int, int]

REGEX: str = r"^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$"
WIDTH: int = 101
HEIGHT: int = 103


def read_input(filepath: str) -> Iterator[tuple[XY, XY]]:
    with open(filepath, "r") as file:
        robots: list[str] = file.read().splitlines()
    for robot in robots:
        re_match: Match[str] | None = match(REGEX, robot)
        if re_match is None:
            raise ValueError(f"Invalid line: {robot}")
        position: XY = (int(re_match.group(1)), int(re_match.group(2)))
        velocity: XY = (int(re_match.group(3)), int(re_match.group(4)))
        yield position, velocity


def _position(position: XY, velocity: XY, seconds: int) -> XY:
    x: int = (position[0] + velocity[0] * seconds) % WIDTH
    y: int = (position[1] + velocity[1] * seconds) % HEIGHT
    return x, y


def _positions(robots: list[tuple[XY, XY]], seconds: int) -> Iterator[XY]:
    logging.debug(f"Seconds: {seconds}")
    for robot in robots:
        end_position: XY = _position(robot[0], robot[1], seconds)
        yield end_position


def main(input_path: str) -> int:
    robots: list[tuple[XY, XY]] = list(read_input(input_path))
    seconds: int = 1
    while True:
        positions: list[XY] = list(_positions(robots, seconds))
        if len(positions) == len(set(positions)):
            logging.debug(f"Positions: {positions}")
            break
        seconds += 1
    return seconds


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    seconds: int = main(args.path[0])
    print(f"The number of seconds until tree is: {seconds}")
