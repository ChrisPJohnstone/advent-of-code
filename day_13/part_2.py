#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Iterator
from re import Match, match
import logging

type Position = tuple[int, int]

BUTTON_REGEX: str = r"^Button [A|B]: X(\+\d+), Y(\+\d+)$"
PRIZE_REGEX: str = r"^Prize: X=(\d+), Y=(\d+)$"
PRIZE_INCREASE: int = 10000000000000
A_COST: int = 3
B_COST: int = 1


def _read_input(line: str, pattern: str) -> Position:
    re_match: Match[str] | None = match(pattern, line)
    if re_match is None:
        raise ValueError(f"Invalid line: {line}")
    x: int = int(re_match.group(1))
    y: int = int(re_match.group(2))
    return (x, y)


def read_input(filepath: str) -> Iterator[tuple[Position, Position, Position]]:
    with open(filepath, "r") as file:
        machines: list[str] = file.read().split("\n\n")
    for machine in machines:
        split: list[str] = machine.splitlines()
        a: Position = _read_input(split[0], BUTTON_REGEX)
        b: Position = _read_input(split[1], BUTTON_REGEX)
        prize: Position = _read_input(split[2], PRIZE_REGEX)
        yield a, b, (prize[0] + PRIZE_INCREASE, prize[1] + PRIZE_INCREASE)


def tokens_to_prize(p: Position, a: Position, b: Position) -> int:
    """
    I had to cheat on this one because I couldn't figure out an algorithm.
    Apparently we need to use Cramer's rule to solve the system of equations
    I got the formula from this reddit thread:
    https://www.reddit.com/r/adventofcode/comments/1hd7irq/2024_day_13_an_explanation_of_the_mathematics/
    """
    times_b: float = (p[1] * a[0] - p[0] * a[1]) / (b[1] * a[0] - b[0] * a[1])
    if times_b < 0 or not times_b.is_integer():
        logging.debug(f"Invalid times_b: {times_b}")
        return 0
    times_a: float = (p[0] - b[0] * times_b) / a[0]
    if times_a < 0 or not times_a.is_integer():
        logging.debug(f"Invalid times_a: {times_a}")
        return 0
    return int(times_a) * A_COST + int(times_b) * B_COST


def main(input_path: str) -> int:
    output: int = 0
    for machine in read_input(input_path):
        logging.debug(f"Machine: {machine}")
        output += tokens_to_prize(machine[2], machine[0], machine[1])
    return output


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    tokens: int = main(args.path[0])
    print(f"The number of tokens is: {tokens}")
