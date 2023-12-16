from queue import Queue
from typing import List, NamedTuple, Tuple

INPUT = "input16.txt"
TEST = "test16.txt"
START = (0, 0)

# DIAGONALS = {
#     "/": {
#         (0, 1): (-1, 0),
#         (1, 0): (0, -1),
#         (0, -1): (1, 0),
#         (-1, 0): (0, 1)
#     },
#     "\\": {
#         (0, 1): (1, 0),
#         (1, 0): (0, 1),
#         (0, -1): (-1, 0),
#         (-1, 0): (0, -1)
#     }
# }


class Position(NamedTuple):
    coords: Tuple[int, int]
    direction: Tuple[int, int]


def get_grid(file: str) -> List[List[str]]:
    grid = []
    with open(file, 'r') as f_in:
        for line in f_in:
            grid.append([x for x in line.strip()])
    return grid


def is_out_of_bounds(pos: Tuple[int, int], grid: List[List[str]]) -> bool:
    return pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[0])


def move_in_direction(coords: Tuple[int, int], direction: Tuple[int, int]) -> Tuple[int, int]:
    return coords[0] + direction[0], coords[1] + direction[1]


def get_new_positions(pos: Position, grid: List[List[str]]) -> List[Position]:
    symbol = grid[pos.coords[0]][pos.coords[1]]

    if symbol == ".":
        # just pass through in current direction
        return [Position(move_in_direction(pos.coords, pos.direction), pos.direction)]
    elif symbol == "|":
        if pos.direction in ((1, 0), (-1, 0)):
            # pass through
            return [Position(move_in_direction(pos.coords, pos.direction), pos.direction)]
        else:
            return [
                Position(move_in_direction(pos.coords, (1, 0)), (1, 0)),
                Position(move_in_direction(pos.coords, (-1, 0)), (-1, 0)),
                ]
    elif symbol == "-":
        if pos.direction in ((0, 1), (0, -1)):
            return [Position(move_in_direction(pos.coords, pos.direction), pos.direction)]
        else:
            return [
                Position(move_in_direction(pos.coords, (0, 1)), (0, 1)),
                Position(move_in_direction(pos.coords, (0, -1)), (0, -1)),
                ]
    elif symbol == "/":
        new_direction = -pos.direction[1], -pos.direction[0]
        return [Position(move_in_direction(pos.coords, new_direction), new_direction)]
    elif symbol == "\\":
        new_direction = pos.direction[1], pos.direction[0]
        return [Position(move_in_direction(pos.coords, new_direction), new_direction)]


def get_energized_count(grid: List[List[str]], start=Position((0, 0), (0, 1))) -> int:
    # just track unique tiles passed through
    energized = set()
    positions_checked = set()

    to_process = Queue()
    to_process.put(start)

    while not to_process.empty():
        current = to_process.get()
        if is_out_of_bounds(current.coords, grid) or current in positions_checked:
            continue
        else:
            energized.add(current.coords)
            positions_checked.add(current)

        # work out next positions from here: pass through, split or 90 deg rotation
        next_paths = get_new_positions(current, grid)
        # print(f"{current.coords} -> {next_paths}")
        for p in next_paths:
            to_process.put(p)

    print(f"Energized {len(energized)} for start {start}")
    return len(energized)


def main1():
    grid = get_grid(INPUT)
    energized = get_energized_count(grid)
    print(f"Energized: {energized} tiles")


def main2():
    grid = get_grid(INPUT)

    max_energized = 0
    max_energized_start = None
    for col in range(len(grid)):
        # ->
        start = Position((col, 0), (0, 1))
        energized = get_energized_count(grid, start)
        if energized > max_energized:
            max_energized_start = start
            max_energized = energized

        # <-
        start = Position((col, len(grid[0]) - 1), (0, -1))
        energized = get_energized_count(grid, start)
        if energized > max_energized:
            max_energized_start = start
            max_energized = energized

    for col in range(len(grid[0])):
        # down
        start = Position((0, col), (1, 0))
        energized = get_energized_count(grid, start)
        if energized > max_energized:
            max_energized_start = start
            max_energized = energized

        # up
        start = Position((len(grid) - 1, col), (-1, 0))
        energized = get_energized_count(grid, start)
        if energized > max_energized:
            max_energized_start = start
            max_energized = energized

    print(f"Max energized = {max_energized} for start {max_energized_start}")


if __name__ == "__main__":
    main2()
