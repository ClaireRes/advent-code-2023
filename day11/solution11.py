from typing import NamedTuple, Set

INPUT = "input11.txt"
TEST = "test11.txt"


class Galaxy(NamedTuple):
    row: int
    col: int


class Map(NamedTuple):
    galaxies: Set[Galaxy]
    rows_occupied: Set[int]
    cols_occupied: Set[int]
    num_rows: int
    num_cols: int


def get_map(file: str) -> Map:
    galaxies = set()
    rows_occupied = set()
    cols_occupied = set()
    with open(file, 'r') as f_in:
        for row, line in enumerate(f_in):
            for col, x in enumerate(line.strip()):
                if x == '#':
                    galaxies.add(Galaxy(row, col))
                    rows_occupied.add(row)
                    cols_occupied.add(col)

    num_rows = row + 1
    num_cols = col + 1
    return Map(
        galaxies,
        rows_occupied=rows_occupied,
        cols_occupied=cols_occupied,
        num_rows=num_rows,
        num_cols=num_cols)


def expand_map(galaxy_map: Map) -> Map:
    # for every col expanded, shift galaxies on rhs +1
    # for every row expanded, shift galaxies below +1
    shift_factor = 1000000
    row_shift = []
    shift = 0
    for i in range(galaxy_map.num_rows):
        row_shift.append(shift)
        if i not in galaxy_map.rows_occupied:
            shift += (shift_factor - 1)

    col_shift = []
    shift = 0
    for j in range(galaxy_map.num_cols):
        col_shift.append(shift)
        if j not in galaxy_map.cols_occupied:
            shift += (shift_factor - 1)

    shifted_galaxies = set()
    for g in galaxy_map.galaxies:
        shifted_g = Galaxy(g.row + row_shift[g.row], g.col + col_shift[g.col])
        shifted_galaxies.add(shifted_g)

    return Map(shifted_galaxies, galaxy_map.rows_occupied,
               galaxy_map.cols_occupied, galaxy_map.num_rows + row_shift[-1],
               galaxy_map.num_cols + col_shift[-1])


def get_path_lengths(galaxy_map: Map):
    galaxies = list(galaxy_map.galaxies)
    total = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1:]:
            # L1 distance = mod(x_delta) + mod(y_delta)
            distance = abs(g1.row - g2.row) + abs(g1.col - g2.col)
            total += distance

    print(f"Total distance = {total}")


def main1():
    # get galaxy grid
    # work out empty rows and columns which need doubling
    # work out shortest path between each pair = L1 distance
    galaxy_map = get_map(INPUT)
    shifted_map = expand_map(galaxy_map)
    get_path_lengths(shifted_map)


if __name__ == "__main__":
    main1()
