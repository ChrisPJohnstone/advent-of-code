#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from collections.abc import Iterator
import logging

type Blocks = list[tuple[str, int]]


def read_input(filepath: str) -> list[str]:
    with open(filepath, "r") as file:
        output: list[str] = list(file.read()[:-1])
    logging.debug(f"Disk map: {output}")
    return output


def _blocks(disk_map: list[str]) -> Blocks:
    """
    Returns [(block: size)]
    """
    blocks: Blocks = []
    file_position: int = 0
    for n, file_size in enumerate(disk_map):
        if file_size == "0":
            continue
        if n % 2 == 0:
            block: str = str(file_position)
            file_position += 1
        else:
            block: str = "."
        blocks.append((block, int(file_size)))
    logging.debug(f"Blocks: {blocks}")
    return blocks


def _compact(disk_map: list[str]) -> Blocks:
    blocks: Blocks = _blocks(disk_map)
    rev_blocks: Blocks = blocks[::-1]
    for rev_char, rev_size in rev_blocks:
        logging.debug("".join([char * size for char, size in blocks]))
        for n, block in enumerate(blocks):
            char, size = block
            if char == rev_char:
                break
            if char != ".":
                continue
            if size < rev_size:
                continue
            swap_n: int = blocks.index((rev_char, rev_size))
            blocks[swap_n] = (".", rev_size)
            blocks[n] = (rev_char, rev_size)
            if size != rev_size:
                blocks.insert(n + 1, (char, size - rev_size))
            break
    return blocks


def compact(disk_map: list[str]) -> Iterator[int]:
    blocks: Blocks = _compact(disk_map)
    position: int = 0
    for char, size in blocks:
        for _ in range(size):
            if char != ".":
                yield int(char) * position
            position += 1


def main(input_path: str) -> int:
    disk_map: list[str] = read_input(input_path)
    checksum: int = 0
    for block in compact(disk_map):
        checksum += block
    return checksum


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    checksum: int = main(args.path[0])
    print(f"The total checksum is {checksum}")
