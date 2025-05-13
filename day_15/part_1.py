#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from itertools import chain
import logging

type XY = tuple[int, int]


class Warehouse:
    BOX_CHAR: str = "O"
    EMPTY_CHAR: str = "."
    ROBOT_CHAR: str = "@"
    WALL_CHAR: str = "#"
    MOVES: dict[str, Callable[[XY], XY]] = {
        "^": lambda pos: (pos[0], pos[1] - 1),
        "v": lambda pos: (pos[0], pos[1] + 1),
        "<": lambda pos: (pos[0] - 1, pos[1]),
        ">": lambda pos: (pos[0] + 1, pos[1]),
    }

    def __init__(self, warehouse_map: list[str]) -> None:
        self._warehouse_map: list[str] = warehouse_map
        self.reset()

    def __str__(self) -> str:
        string: str = ""
        for y in range(len(self._warehouse_map)):
            for x in range(len(self._warehouse_map[0])):
                if (x, y) == self.robot_position:
                    string += self.ROBOT_CHAR
                elif (x, y) in self.boxes:
                    string += self.BOX_CHAR
                elif (x, y) in self.walls:
                    string += self.WALL_CHAR
                else:
                    string += self.EMPTY_CHAR
            string += "\n"
        return string

    @property
    def walls(self) -> set[XY]:
        return self._walls

    @property
    def boxes(self) -> set[XY]:
        return self._boxes

    @property
    def robot_position(self) -> XY:
        return self._robot_position

    def reset(self) -> None:
        self._walls: set[XY] = set()
        self._boxes: set[XY] = set()
        for y, row in enumerate(self._warehouse_map):
            for x, char in enumerate(row):
                if char == self.WALL_CHAR:
                    self._walls.add((x, y))
                elif char == self.BOX_CHAR:
                    self._boxes.add((x, y))
                elif char == self.ROBOT_CHAR:
                    self._robot_position = (x, y)

    def move_box(self, box: XY, move_func: Callable[[XY], XY]) -> bool:
        new_position: XY = move_func(box)
        logging.debug(f"Moving box {box} to {new_position}")
        if new_position in self.walls:
            logging.debug(f"Aborting move to wall {new_position}")
            return False
        if new_position in self.boxes:
            if not self.move_box(new_position, move_func):
                return False
        self.boxes.remove(box)
        self.boxes.add(new_position)
        logging.debug(f"Moved box {box} to {new_position}")
        return True

    def move_robot(self, direction: str) -> None:
        logging.debug(f"Moving robot {self.robot_position} {direction}")
        move_func: Callable[[XY], XY] = Warehouse.MOVES[direction]
        new_position: XY = move_func(self._robot_position)
        if new_position in self.walls:
            logging.debug(f"Aborting move to wall {new_position}")
            return
        if new_position in self.boxes:
            if not self.move_box(new_position, move_func):
                logging.debug(f"Aborting move to box {new_position}")
                return
        logging.debug(f"Moved robot {self._robot_position} to {new_position}")
        self._robot_position = new_position

    def make_moves(self, moves: list[str]) -> None:
        for move in moves:
            self.move_robot(move)

    @staticmethod
    def box_coordinate(box: XY) -> int:
        return box[1] * 100 + box[0]

    def sum_coordinates(self) -> int:
        return sum(Warehouse.box_coordinate(box) for box in self.boxes)


def read_input(filepath: str) -> tuple[list[str], list[str]]:
    with open(filepath, "r") as file:
        parts: list[str] = file.read().split("\n\n")
    warehouse: list[str] = parts[0].splitlines()
    moves: list[str] = list(chain(*parts[1].splitlines()))
    return warehouse, moves


def main(input_path: str) -> int:
    parts: tuple[list[str], list[str]] = read_input(input_path)
    warehouse: Warehouse = Warehouse(parts[0])
    warehouse.make_moves(parts[1])
    return warehouse.sum_coordinates()


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="path", nargs=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    output: int = main(args.path[0])
    print(f"The sum of coordinates is: {output}")
