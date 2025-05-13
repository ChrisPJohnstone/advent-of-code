#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from itertools import chain
import logging

type XY = tuple[int, int]


class Warehouse:
    BOX_CHAR: str = "O"
    BOX_CHAR_WIDE: str = "[]"
    EMPTY_CHAR: str = "."
    EMPTY_CHAR_WIDE: str = ".."
    ROBOT_CHAR: str = "@"
    ROBOT_CHAR_WIDE: str = "@."
    WALL_CHAR: str = "#"
    WALL_CHAR_WIDE: str = "##"
    MOVES: dict[str, Callable[[XY], XY]] = {
        "^": lambda pos: (pos[0], pos[1] - 1),
        "v": lambda pos: (pos[0], pos[1] + 1),
        "<": lambda pos: (pos[0] - 1, pos[1]),
        ">": lambda pos: (pos[0] + 1, pos[1]),
    }

    def __init__(self, warehouse_map: list[str]) -> None:
        self._warehouse_map: list[str] = Warehouse.widen_map(warehouse_map)
        self.reset()

    def __str__(self) -> str:
        string: str = ""
        for y in range(len(self._warehouse_map)):
            for x in range(len(self._warehouse_map[0])):
                if (x - 1, y) in self.boxes:
                    continue
                elif (x, y) == self.robot_position:
                    string += self.ROBOT_CHAR
                elif (x, y) in self.boxes:
                    string += self.BOX_CHAR_WIDE
                elif (x, y) in self.walls:
                    string += self.WALL_CHAR
                else:
                    string += self.EMPTY_CHAR
            string += "\n"
        return string

    @staticmethod
    def widen_map(warehouse_map: list[str]) -> list[str]:
        new_map: list[str] = []
        for row in warehouse_map:
            new_line: str = ""
            for char in row:
                match char:
                    case Warehouse.WALL_CHAR:
                        new_line += Warehouse.WALL_CHAR_WIDE
                    case Warehouse.BOX_CHAR:
                        new_line += Warehouse.BOX_CHAR_WIDE
                    case Warehouse.EMPTY_CHAR:
                        new_line += Warehouse.EMPTY_CHAR_WIDE
                    case Warehouse.ROBOT_CHAR:
                        new_line += Warehouse.ROBOT_CHAR_WIDE
            new_map.append(new_line)
        return new_map

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
                elif char == self.BOX_CHAR_WIDE[0]:
                    self._boxes.add((x, y))
                elif char == self.ROBOT_CHAR:
                    self._robot_position = (x, y)

    def can_box_move(self, box: XY, direction: str) -> bool:
        logging.debug(f"Can box {box} move {direction}")
        move_func: Callable[[XY], XY] = Warehouse.MOVES[direction]
        new_l: XY = move_func(box)
        new_r: XY = (new_l[0] + 1, new_l[1])
        if {new_l, new_r} & self.walls:
            return False
        if direction == "<":
            possibles: set[XY] = {(new_l[0] - 1, new_l[1])}
        elif direction == ">":
            possibles: set[XY] = {new_r}
        else:
            possibles: set[XY] = {(new_l[0] - 1, new_l[1]), new_l, new_r}
        boxes: set[XY] = possibles & self.boxes
        if not boxes:
            return True
        return all(self.can_box_move(new_box, direction) for new_box in boxes)

    def move_box(self, box: XY, direction: str) -> None:
        move_func: Callable[[XY], XY] = Warehouse.MOVES[direction]
        new: XY = move_func(box)
        if direction == "<":
            possibles: set[XY] = {(new[0] - 1, new[1])}
        elif direction == ">":
            possibles: set[XY] = {(new[0] + 1, new[1])}
        else:
            possibles: set[XY] = {
                (new[0] - 1, new[1]),
                new,
                (new[0] + 1, new[1]),
            }
        next_boxes: set[XY] = possibles & self.boxes
        for next_box in next_boxes:
            self.move_box(next_box, direction)
        self.boxes.remove(box)
        self.boxes.add(new)
        logging.debug(f"Moved box {box} to {new}")

    def move_robot(self, direction: str) -> None:
        logging.debug(f"Moving robot {self.robot_position} {direction}")
        move_func: Callable[[XY], XY] = Warehouse.MOVES[direction]
        new_position: XY = move_func(self._robot_position)
        if new_position in self.walls:
            logging.debug(f"Aborting move to wall {new_position}")
            return
        box_positions: set[XY] = set()
        if direction == "<":
            box_positions: set[XY] = {(new_position[0] - 1, new_position[1])}
        else:
            box_positions: set[XY] = {new_position}
            if direction != ">":
                box_positions.add((new_position[0] - 1, new_position[1]))
        if box_position := box_positions & self.boxes:
            if not self.can_box_move(list(box_position)[0], direction):
                return
            self.move_box(list(box_position)[0], direction)
        logging.debug(f"Moved robot {self._robot_position} to {new_position}")
        self._robot_position = new_position

    def make_moves(self, moves: list[str]) -> None:
        print(self)
        for n, move in enumerate(moves):
            logging.debug(f"Move: {n}, {move}")
            self.move_robot(move)
        print(self)

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
