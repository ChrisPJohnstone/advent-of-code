#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Iterator
import logging

type Plot = tuple[int, int]
type PlotMap = dict[Plot, str]
type Region = set[Plot]

DIRECTIONS: list[Callable] = [
    lambda x, y: (x, y - 1),  # Up
    lambda x, y: (x, y + 1),  # Down
    lambda x, y: (x - 1, y),  # Up
    lambda x, y: (x + 1, y),  # Right
]


def read_input(filepath: str) -> Iterator[tuple[Plot, str]]:
    with open(filepath, "r") as file:
        for y, line in enumerate(file.read().splitlines()):
            for x, char in enumerate(line):
                yield (x, y), char


def _region(plot_map: PlotMap, plot: Plot) -> Iterator[Plot]:
    yield plot
    char: str = plot_map[plot]
    del plot_map[plot]
    for direction in DIRECTIONS:
        new_plot: Plot = direction(*plot)
        if char == plot_map.get(new_plot):
            yield from _region(plot_map, new_plot)


def regions(plot_map: PlotMap) -> Iterator[Region]:
    for plot in list(plot_map.keys()):
        if plot not in plot_map.keys():
            continue
        plant: str = plot_map[plot]
        region: Region = set(_region(plot_map, plot))
        logging.debug(f"Plant {plant} Region {region}")
        yield region


def _perimeter(region: Region, plot: Plot) -> int:
    output: int = 4
    for direction in DIRECTIONS:
        new_plot: Plot = direction(*plot)
        if new_plot in region:
            output -= 1
    return output


def perimeter(region: Region) -> int:
    output: int = 0
    for plot in region:
        output += _perimeter(region, plot)
    return output


def main(input_path: str) -> int:
    plot_map: PlotMap = dict(read_input(input_path))
    price: int = 0
    for region in regions(plot_map):
        price += len(region) * perimeter(region)
    return price


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    price: int = main(args.path[0])
    print(f"Total price {price}")
