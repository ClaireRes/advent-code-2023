INPUT = "input9.txt"
TEST_INPUT = "testinput9.txt"


def extrapolate_readings(readings: list) -> int:
    last_differences = []

    print("\n")
    values = readings
    current_differences = [values[i] - values[i-1] for i in range(1, len(values))]
    while any(i != 0 for i in current_differences):
        print(current_differences)
        last_differences.append(current_differences[-1])
        values = current_differences
        current_differences = [values[i] - values[i - 1] for i in range(1, len(values))]

    # extrapolate
    extrapolated = sum(last_differences) + readings[-1]
    print(f"last diffs {last_differences} -> {extrapolated}")
    return extrapolated


def extrapolate_readings_backwards(readings: list) -> int:
    first_differences = []

    print("\n")
    values = readings
    print(readings)
    current_differences = [values[i] - values[i-1] for i in range(1, len(values))]
    while any(i != 0 for i in current_differences):
        print(current_differences)
        first_differences.append(current_differences[0])
        values = current_differences
        current_differences = [values[i] - values[i - 1] for i in range(1, len(values))]

    # extrapolate
    diff = 0
    for d in first_differences[::-1]:
        diff = d - diff

    extrapolated = readings[0] - diff
    print(f"extrapolated = {extrapolated}")
    return extrapolated


def main1():
    extrapolated = []
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            readings = [int(x) for x in line.strip().split()]
            extrapolated.append(extrapolate_readings(readings))

    print(f"total is {sum(extrapolated)}")


def main2():
    extrapolated = []
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            readings = [int(x) for x in line.strip().split()]
            extrapolated.append(extrapolate_readings_backwards(readings))

    print(f"total is {sum(extrapolated)}")


if __name__ == "__main__":
    main2()
