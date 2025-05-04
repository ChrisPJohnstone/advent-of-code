#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from collections.abc import Callable
import logging


def read_input(filepath: str) -> list[int]:
    logging.debug(f"Reading {filepath}")
    with open(filepath, "r") as file:
        lines: list[str] = file.read().splitlines()
    for line in lines:
        yield [int(value) for value in line.split(" ")]


def _is_report_valid(report: list[int]) -> bool:
    if report[1] > report[0]:
        is_dir_valid: Callable = lambda prev, curr: prev < curr
    else:
        is_dir_valid: Callable = lambda prev, curr: prev > curr
    for n in range(1, len(report)):
        prev: int = report[n - 1]
        curr: int = report[n]
        distance: int = abs(prev - curr)
        if distance < 1 or distance > 3:
            logging.debug(f"-- Report {report} {prev} {curr} invalid distance")
            return False
        if not is_dir_valid(prev, curr):
            logging.debug(f"-- Report {report} {prev} {curr} changes direction")
            return False
    logging.debug(f"++ Report {report}")
    return True


def is_report_valid(report: list[int]) -> bool:
    logging.debug(f"Checking {report}")
    for n in range(len(report)):
        if _is_report_valid(report[:n] + report[n + 1 :]):
            return True
    return False


def main(input_path: str) -> int:
    safe_reports: int = 0
    for report in read_input(input_path):
        valid: bool = is_report_valid(report)
        if valid:
            safe_reports += 1
    return safe_reports


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    safe: int = main(args.path[0])
    print(f"The number of safe reports is: {safe}")
