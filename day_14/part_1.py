#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Iterator
from math import prod
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


def positions(robots: list[tuple[XY, XY]], seconds: int) -> Iterator[XY]:
    logging.debug(f"Seconds: {seconds}")
    for n, robot in enumerate(robots):
        end_position: XY = _position(robot[0], robot[1], seconds)
        logging.debug(f"Robot {n}: {robot[0]} -> {end_position}. V: {robot[1]}")
        yield end_position


def _quadrant(x: int, y: int) -> int:
    """
    Returns the quadrant of the given coordinates.
    0: top left
    1: top right
    2: bottom left
    3: bottom right
    4: center
    """
    mid_x: int = WIDTH // 2
    mid_y: int = HEIGHT // 2
    if x == mid_x or y == mid_y:
        return 4
    if x < mid_x:
        return 0 if y < mid_y else 2
    return 1 if y < mid_y else 3


def main(input_path: str, seconds: int) -> int:
    robots: list[tuple[XY, XY]] = list(read_input(input_path))
    quadrants: list[int] = [0, 0, 0, 0]
    for position in positions(robots, seconds):
        quadrant: int = _quadrant(position[0], position[1])
        logging.debug(f"Position: {position}, Quadrant: {quadrant}")
        if quadrant == 4:
            continue
        quadrants[quadrant] += 1
    logging.debug(f"Quadrants: {quadrants}")
    return prod(quadrants)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument(dest="seconds", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    factor: int = main(args.path[0], int(args.seconds[0]))
    print(f"The safety factor is: {factor}")
