import string
from collections import defaultdict


INPUT = "input3.txt"
DIGITS = {*string.digits}
PERIOD = '.'
ASTERISK = '*'


# Return a two by two array
def build_grid() -> list:
    grid = []
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            row = [*line.strip()]
            grid.append(row)
    return grid

# Find all numbers adjacent to a symbol in NxN grid.
# Scan through grid for numbers, track when we hit start
# of a number. For each digit, check if it's adjacent.
# If it is, carry scanning until get to end row or non-digit,
# then return that number.


def is_adjacent_to_symbol(grid: list, i: int, j: int) -> bool:
    num_rows = len(grid)
    num_cols = len(grid[0])

    # Check 8-cell border of value(i, j)
    for row_num in (i-1, i, i+1):
        for col_num in (j-1, j, j+1):
            if row_num < 0 or row_num >= num_rows or col_num < 0 or col_num >= num_cols:
                continue
            if (row_num, col_num) == (i, j):
                continue
            value = grid[row_num][col_num]
            if value != PERIOD and value not in DIGITS:
                # assume only other values are symbols
                return True
    return False


def get_numbers_adjacent_to_symbols(grid: list) -> list:
    found = []
    # track start col of current number
    num_start_col = -1
    current_num_is_adjacent = False
    num_cols = len(grid[0])
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char in DIGITS:
                if num_start_col < 0:
                    num_start_col = j
                if not current_num_is_adjacent:
                    current_num_is_adjacent = is_adjacent_to_symbol(grid, i, j)
            else:
                # Handle non-digit after run of numbers
                if num_start_col >= 0 and current_num_is_adjacent:
                    # Add last number run (up to current, non-inclusive)
                    found.append(int(''.join(row[num_start_col:j])))
                # Reset for next run of numbers
                num_start_col = -1
                current_num_is_adjacent = False

        if num_start_col >= 0 and current_num_is_adjacent:
            # Add last number run (up to current, non-inclusive)
            found.append(int(''.join(row[num_start_col:num_cols])))
        # Reset for next row
        num_start_col = -1
        current_num_is_adjacent = False

    return found


"""
A gear is any * symbol that is adjacent to exactly two part numbers.
Its gear ratio is the result of multiplying those two numbers together.
This time, you need to find the gear ratio of every gear and add them
all up so that the engineer can figure out which gear needs to be replaced.
"""


def get_adjacent_asterisks(grid: list, i: int, j: int) -> list:
    num_rows = len(grid)
    num_cols = len(grid[0])
    adjacent = []

    # Check 8-cell border of value(i, j)
    for row_num in (i-1, i, i+1):
        for col_num in (j-1, j, j+1):
            if row_num < 0 or row_num >= num_rows or col_num < 0 or col_num >= num_cols:
                continue
            if (row_num, col_num) == (i, j):
                continue
            value = grid[row_num][col_num]
            if value == ASTERISK:
                adjacent.append((row_num, col_num))

    return adjacent


def find_asterisk_adjacent_numbers(grid: list) -> dict:
    # Need to keep track of mapping of * coords -> numbers adjacent then filter to only *'s with 2 numbers
    asterisk_adjacent_numbers = defaultdict(list)

    # track start col of current number
    num_start_col = -1
    current_adjacent_asterisks = set()
    num_cols = len(grid[0])
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char in DIGITS:
                if num_start_col < 0:
                    num_start_col = j

                for coords in get_adjacent_asterisks(grid, i, j):
                    current_adjacent_asterisks.add(coords)
            else:
                # Handle non-digit after run of numbers
                if num_start_col >= 0 and current_adjacent_asterisks:
                    num = int(''.join(row[num_start_col:j]))
                    for coords in current_adjacent_asterisks:
                        asterisk_adjacent_numbers[coords].append(num)

                # Reset for next run of numbers
                num_start_col = -1
                current_adjacent_asterisks = set()

        # Reset for end of row
        if num_start_col >= 0 and current_adjacent_asterisks:
            num = int(''.join(row[num_start_col:num_cols]))
            for coords in current_adjacent_asterisks:
                asterisk_adjacent_numbers[coords].append(num)

        # Reset for next run of numbers
        num_start_col = -1
        current_adjacent_asterisks = set()

    return asterisk_adjacent_numbers


def main1():
    grid = build_grid()
    num_rows = len(grid)
    num_cols = len(grid[0])

    print(f"Grid = {num_rows} rows x {num_cols} columns")

    parts = get_numbers_adjacent_to_symbols(grid)
    print(f"Parts: {parts}")
    print(f"Sum of parts = {sum(parts)}")


def find_gear_ratios(asterisk_to_nums: dict):
    gear_ratios = []
    for coords, adjacent_nums in asterisk_to_nums.items():
        if len(adjacent_nums) == 2:
            ratio = adjacent_nums[0] * adjacent_nums[1]
            print(f"Gear at {coords} for {adjacent_nums} = {ratio}")
            gear_ratios.append(ratio)
    return gear_ratios


def main2():
    grid = build_grid()
    num_rows = len(grid)
    num_cols = len(grid[0])

    print(f"Grid = {num_rows} rows x {num_cols} columns")

    asterisk_to_nums = find_asterisk_adjacent_numbers(grid)
    gear_ratios = find_gear_ratios(asterisk_to_nums)
    print(f"Sum of gear ratios = {sum(gear_ratios)}")


if __name__ == "__main__":
    main2()
