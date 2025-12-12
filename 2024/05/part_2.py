#!/usr/bin/env python
from argparse import ArgumentParser, Namespace


def read_input(filepath: str) -> tuple[dict[int, set[int]], list[list[int]]]:
    with open(filepath, "r") as file:
        lines: list[str] = file.readlines()
    rules: dict[int, set[int]] = {}
    updates: list[list[int]] = []
    for line in lines:
        if "|" in line:
            pages: list[str] = line[:-1].split("|")
            key: int = int(pages[0])
            if key not in rules:
                rules[key] = set()
            rules[key].add(int(pages[1]))
        if "," in line:
            update: list[int] = [int(page) for page in line[:-1].split(",")]
            updates.append(update)
    return rules, updates


def is_valid_update(rules: dict[int, set[int]], update: list[int]) -> bool:
    for n in range(1, len(update)):
        previous_pages: set[int] = set(update[:n])
        forbidden_pages: set[int] = rules.get(update[n], set())
        if previous_pages & forbidden_pages:
            return False
    return True


def fix_update(rules: dict[int, set[int]], update: list[int]) -> list[int]:
    n: int = 1
    while n < len(update):
        page: int = update[n]
        previous_pages: set[int] = set(update[:n])
        forbidden_pages: set[int] = rules.get(page, set())
        invalid_pages: set[int] = previous_pages & forbidden_pages
        if not invalid_pages:
            n += 1
            continue
        for invalid_page in invalid_pages:
            position: int = update.index(invalid_page)
            update.pop(position)
            update.insert(n, invalid_page)
        n: int = update.index(page) + 1
    return update


def main(input_path: str) -> int:
    rules, updates = read_input(input_path)
    counter: int = 0
    for update in updates:
        if is_valid_update(rules, update):
            continue
        fixed_update: list[int] = fix_update(rules, update)
        counter += fixed_update[int(len(fixed_update) / 2)]
    return counter


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    args: Namespace = parser.parse_args()
    total: int = main(args.path[0])
    print(f"The sum of middle digits is {total}")
