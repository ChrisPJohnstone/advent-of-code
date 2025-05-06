#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Iterator
from itertools import combinations
import logging

type EquationsType = list[tuple[int, list[int]]]


def read_input(filepath: str) -> EquationsType:
    with open(filepath, "r") as file:
        lines: list[str] = file.read().splitlines()
    equations: EquationsType = [
        (
            int(line[: line.find(":")]),
            [int(value) for value in line[line.find(":") + 2 :].split(" ")],
        )
        for line in lines
    ]
    return equations


def all_mul_positions(n_parts: int) -> Iterator[set[int]]:
    yield {-1}
    possible_positions: range = range(1, n_parts)
    for n in possible_positions:
        yield {n}
    for n in range(2, n_parts):
        for combination in combinations(possible_positions, n):
            yield set(combination)


def _calculate_equation(parts: list[int], mul_positions: set[int]) -> int:
    product: int = parts[0]
    equation: list[str] = [str(parts[0])]
    for n in range(1, len(parts)):
        if n in mul_positions:
            equation.append("*")
            product *= parts[n]
        else:
            equation.append("+")
            product += parts[n]
        equation.append(str(parts[n]))
    logging.debug(f"{''.join(equation)} = {product}")
    return product


def calculate_equation(target: int, parts: list[int]) -> int:
    log_result: Callable = lambda x: logging.debug(f"{x} {target} from {parts}")
    for mul_positions in all_mul_positions(len(parts)):
        product: int = _calculate_equation(parts, mul_positions)
        if product == target:
            log_result("+")
            return target
    log_result("-")
    return 0


def main(input_path: str) -> int:
    equations: EquationsType = read_input(input_path)
    total: int = 0
    for equation in equations:
        total += calculate_equation(*equation)
    return total


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    result: int = main(args.path[0])
    print(f"The calibration result is {result}")
