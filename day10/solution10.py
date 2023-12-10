from queue import Queue
from typing import NamedTuple, List

INPUT = "input10.txt"
TEST_3 = "testinput10.txt"
TEST_1 = 'test1.txt'
TEST_2 = 'test2.txt'
START = 'S'


class Coords(NamedTuple):
    row: int
    col: int


class NodeToVisit(NamedTuple):
    coords: Coords
    previous: list[Coords]


class Grid(NamedTuple):
    grid: list
    start: Coords


def process_grid(file: str) -> Grid:
    grid = []
    start = None
    with open(file, 'r') as f_in:
        for i, line in enumerate(f_in):
            row = [c for c in line.strip()]
            if not start and START in row:
                start = Coords(i, row.index(START))
            grid.append(row)
    return Grid(grid, start)


DIRECTIONS = {
    '|': [(1, 0), (-1, 0)],
    '-': [(0, 1), (0, -1)],
    'F': [(1, 0), (0, 1)],
    '7': [(1, 0), (0, -1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    'S': [(-1, 0), (0, 1), (1, 0), (0, -1)]
}


def is_connected(symbol: str, coords: Coords, start: Coords) -> bool:
    directions = DIRECTIONS.get(symbol, [])
    for delta in directions:
        adjacent = Coords(coords.row + delta[0], coords.col + delta[1])
        if adjacent == start:
            return True
    return False


def get_neighbours_to_visit(current: NodeToVisit, grid: Grid) -> List[NodeToVisit]:
    # current_symbol = grid.grid[current.coords.row][current.coords.col]
    # reachable_directions = DIRECTIONS.get(current_symbol, [])
    # num_rows = len(grid.grid)
    # num_cols = len(grid.grid[0])
    #
    # neighbours = []
    # for delta in reachable_directions:
    #     coords = Coords(current.coords.row + delta[0], current.coords.col + delta[1])
    #     if coords.row < 0 or coords.row >= num_rows or coords.col < 0 or coords.col >= num_cols:
    #         continue
    #     # at most two nodes are reachable from current
    #     neighbours.append(NodeToVisit(coords, previous=[*current.previous, current.coords]))

    # # Check N-E-S-W nodes
    num_rows = len(grid.grid)
    num_cols = len(grid.grid[0])
    check_deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbours = []
    for delta in check_deltas:
        coords = Coords(current.coords.row + delta[0], current.coords.col + delta[1])
        if coords.row < 0 or coords.row >= num_rows or coords.col < 0 or coords.col >= num_cols:
            continue
        if current.previous and coords == current.previous[-1]:
            continue

        symbol = grid.grid[coords.row][coords.col]
        if symbol == '.':
            continue
        # both need to connect to each other

        next_to_current = is_connected(symbol, coords, current.coords)
        current_symbol = grid.grid[current.coords.row][current.coords.col]
        if current_symbol == START:
            current_to_next = True
        else:
            current_to_next = is_connected(current_symbol, current.coords, coords)
        if next_to_current and current_to_next:
            neighbours.append(NodeToVisit(coords, previous=[*current.previous, current.coords]))
    return neighbours


def find_loop(grid: Grid):
    # BFS along connected nodes to current node
    # Start from current, explore neighbours and add connected neighbours to queue
    # to explore
    nodes_to_visit = Queue()
    nodes_to_visit.put(NodeToVisit(grid.start, []))
    visited = set()

    prev = None
    current = NodeToVisit(grid.start, [])
    while not nodes_to_visit.empty():
        prev = current
        current = nodes_to_visit.get()
        if current.coords in visited:
            continue

        neighbours = get_neighbours_to_visit(current, grid)
        # print(f"{current.coords} -> {[n.coords for n in neighbours]}")
        for n in neighbours:
            nodes_to_visit.put(n)
        visited.add(current.coords)

    # two branches will meet at furthest point
    loop_path = current.previous
    print(f"Furthest point = {len(loop_path) - 1}")

    complete_loop = [*loop_path, *prev.previous[::-1]]
    return complete_loop


def is_clockwise(loop: List[Coords]):
    turns = {
        ((-1, 0), (0, -1)): -90,    # N->W
        ((-1, 0), (0, 1)): 90,      # N->E
        ((0, 1), (-1, 0)): -90,     # E->N
        ((0, 1), (1, 0)): 90,       # E->S
        ((1, 0), (0, 1)): -90,      # S->E
        ((1, 0), (0, -1)): 90,      # S->E
        ((0, -1), (1, 0)): -90,     # W->S
        ((0, -1), (-1, 0)): 90      # W->N
    }

    degrees = 0
    for i in range(1, len(loop) - 1):
        start = loop[i-1]
        mid = loop[i]
        end = loop[i+1]
        d1 = (mid.row - start.row, mid.col - start.col)
        d2 = (end.row - mid.row, end.col - mid.col)
        deg = turns.get((d1, d2), 0)
        degrees += deg
    print(f"Turned {degrees} degrees")
    return degrees > 0


def find_enclosed(loop: List[Coords], grid: Grid):
    if not is_clockwise(loop):
        # reverse loop direction so we go clockwise round (inside = RHS)
        loop = loop[::-1]

    enclosed = set()
    num_rows = len(grid.grid)
    num_cols = len(grid.grid[0])

    deltas_to_rhs = {
        (0, 1): (1, 0),  # W->E
        (0, -1): (-1, 0),  # E->W
        (1, 0): (0, -1),  # N->S
        (-1, 0): (0, 1)  # S->N
    }

    loop_set = set(loop)
    for i, coords in enumerate(loop):
        if i == len(loop) - 1:
            next_coords = loop[0]
        else:
            next_coords = loop[i+1]
        delta = (next_coords.row - coords.row, next_coords.col - coords.col)
        rhs_delta = deltas_to_rhs.get(delta)
        if not rhs_delta:
            continue

        for k in range(max(num_cols, num_rows)):
            rhs_coords = Coords(coords.row + rhs_delta[0]*(k+1), coords.col + rhs_delta[1]*(k+1))
            # check if we hit boundary of edge or other side of loop
            if rhs_coords.row < 0 or rhs_coords.row >= num_rows or rhs_coords.col < 0 or rhs_coords.col >= num_cols:
                break
            if rhs_coords in loop_set:
                break
            enclosed.add(rhs_coords)
        for k in range(max(num_cols, num_rows)):
            rhs_coords = Coords(next_coords.row + rhs_delta[0]*(k+1), next_coords.col + rhs_delta[1]*(k+1))
            # check if we hit boundary of edge or other side of loop
            if rhs_coords.row < 0 or rhs_coords.row >= num_rows or rhs_coords.col < 0 or rhs_coords.col >= num_cols:
                break
            if rhs_coords in loop_set:
                break
            enclosed.add(rhs_coords)

    print(f"Found {len(enclosed)} enclosed tiles")
    print(enclosed)

    # for i, row in enumerate(grid.grid):
    #     line = ''
    #     for j, c in enumerate(row):
    #         if Coords(i, j) in enclosed:
    #             line += 'I'
    #         else:
    #             symbol = grid.grid[i][j]
    #             line += symbol
    #     print(line)


def main1():
    """
    Find the single giant loop starting at S.
     How many steps along the loop does it take to get from the starting position
      to the point farthest from the starting position?
    """
    grid = process_grid(INPUT)
    # grid = process_grid('part2_test2.txt')
    loop = find_loop(grid)
    find_enclosed(loop, grid)


if __name__ == "__main__":
    main1()
