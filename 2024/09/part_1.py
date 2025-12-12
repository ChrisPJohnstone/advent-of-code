#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from itertools import repeat
import logging


def read_input(filepath: str) -> list[str]:
    with open(filepath, "r") as file:
        output: list[str] = list(file.read()[:-1])
    logging.debug(f"Disk map: {output}")
    return output


def _blocks(disk_map: list[str]) -> list[str]:
    file_position: int = 0
    blocks: list[str] = []
    for n, file_size in enumerate(disk_map):
        if file_size == "0":
            continue
        if n % 2 == 0:
            block: str = str(file_position)
            file_position += 1
        else:
            block: str = "."
        blocks.extend(repeat(block, int(file_size)))
    logging.debug(f"Blocks: {blocks}")
    return blocks


def compact(disk_map: list[str]) -> list[int]:
    blocks: list[str] = _blocks(disk_map)
    rev_blocks: list[str] = list(filter(lambda x: x != ".", blocks[::-1]))
    output: list[int] = []
    total_blocks: int = len(rev_blocks)
    for block in blocks:
        logging.debug(output)
        if len(output) == total_blocks:
            break
        if block != ".":
            output.append(int(block))
            continue
        output.append(int(rev_blocks[0]))
        rev_blocks.pop(0)
    logging.debug(f"Compacted: {''.join(map(str, output))}")
    return output


def main(input_path: str) -> int:
    disk_map: list[str] = read_input(input_path)
    checksum: int = 0
    for n, block in enumerate(compact(disk_map)):
        checksum += block * n
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
