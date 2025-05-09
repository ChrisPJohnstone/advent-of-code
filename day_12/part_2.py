#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Iterator
import logging

type Plot = tuple[int, int]
type PlotMap = dict[Plot, str]
type Region = set[Plot]

DIRECTIONS: list[Callable] = [
    lambda x, y: (x, y - 1),        # N
    lambda x, y: (x + 1, y - 1),    # NE
    lambda x, y: (x + 1, y),        # E
    lambda x, y: (x + 1, y + 1),    # SE
    lambda x, y: (x, y + 1),        # S
    lambda x, y: (x - 1, y + 1),    # SW
    lambda x, y: (x - 1, y),        # W
    lambda x, y: (x - 1, y - 1),    # NW
]
CORNERS: list[Callable] = [
    lambda dirs: not any([dirs[0], dirs[2]]),               # NE Outer
    lambda dirs: not any([dirs[2], dirs[4]]),               # SE Outer
    lambda dirs: not any([dirs[4], dirs[6]]),               # SW Outer
    lambda dirs: not any([dirs[6], dirs[0]]),               # NW Outer
    lambda dirs: all([dirs[0], dirs[2]]) and not dirs[1],   # NE Inner
    lambda dirs: all([dirs[2], dirs[4]]) and not dirs[3],   # SE Inner
    lambda dirs: all([dirs[4], dirs[6]]) and not dirs[5],   # SW Inner
    lambda dirs: all([dirs[6], dirs[0]]) and not dirs[7],   # NW Inner
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
    for n in range(0, len(DIRECTIONS), 2):
        new_plot: Plot = DIRECTIONS[n](*plot)
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


def sides(region: Region) -> int:
    output: int = 0
    for plot in region:
        dirs: list[bool] = [not n(*plot) not in region for n in DIRECTIONS]
        for corner in CORNERS:
            output += int(corner(dirs))
    logging.debug(f"Sides {output}")
    return output


def main(input_path: str) -> int:
    plot_map: PlotMap = dict(read_input(input_path))
    price: int = 0
    for region in regions(plot_map):
        price += len(region) * sides(region)
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
