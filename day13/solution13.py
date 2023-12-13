INPUT = "input13.txt"
# INPUT = "test13.txt"


def is_match_with_smudge(top_or_left: list, bottom_or_right: list) -> bool:
    # can have at most one difference between pairs of lines
    difference = 0
    for t, b in zip(top_or_left, bottom_or_right):
        for tt, bb in zip(t, b):
            if tt != bb:
                if difference:
                    # can only have 1 diff max
                    return False
                difference += 1
    if difference == 1:
        return True
    return False


def get_horizontal_mirror_line(grid: list) -> int:
    for i, row in enumerate(grid):
        if i == (len(grid) - 1):
            break
        # check i from top
        top = grid[:i+1]
        bottom = grid[i+1: (i+1+len(top))][::-1]
        if is_match_with_smudge(top, bottom):
            rows_above = i + 1
            return rows_above

        # check i from bottom
        i_bottom = len(grid) - 1 - i
        bottom = grid[i_bottom:]
        top = grid[i_bottom - len(bottom):i_bottom][::-1]
        if is_match_with_smudge(top, bottom):
            rows_below = len(bottom)
            rows_above = len(grid) - rows_below
            return rows_above
    return -1


def get_vertical_mirror_line(grid: list) -> int:
    num_cols = len(grid[0])
    columns = []
    for j in range(num_cols):
        columns.append(''.join(row[j] for row in grid))

    for i, col in enumerate(columns):
        if i == (len(columns) - 1):
            break
        # check i from left
        left = columns[:i + 1]
        right = columns[i + 1: (i + 1 + len(left))][::-1]
        if is_match_with_smudge(left, right):
            cols_left = i + 1
            return cols_left

        # check i from right
        i_right = len(columns) - 1 - i
        right = columns[i_right:]
        left = columns[i_right - len(right):i_right][::-1]
        if is_match_with_smudge(left, right):
            cols_right = len(right)
            cols_left = len(columns) - cols_right
            return cols_left
    return -1


def get_mirror_line_value(grid: list) -> int:
    """To summarize your pattern notes, add up the number of columns to the
    left of each vertical line of reflection; to that, also add 100 multiplied
     by the number of rows above each horizontal line of reflection"""

    horizontal_line = get_horizontal_mirror_line(grid)
    if horizontal_line >= 0:
        print(f"horizontal mirror line with {horizontal_line} rows above")
        return 100*horizontal_line

    vertical_line = get_vertical_mirror_line(grid)
    if vertical_line >= 0:
        print(f"vertical mirror line with {vertical_line} cols left")
        return vertical_line
    return 0


def main1():
    total = 0
    current_grid = []
    with open(INPUT, 'r') as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                total += get_mirror_line_value(current_grid)
                current_grid = []
            else:
                current_grid.append([x for x in line])
    if current_grid:
        total += get_mirror_line_value(current_grid)

    print(f"Total is: {total}")


if __name__ == "__main__":
    main1()
