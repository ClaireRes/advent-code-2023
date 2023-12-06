import re
from typing import NamedTuple

INPUT = "input6.txt"
PATTERN = r"\s+(\d+)"


class Race(NamedTuple):
    time: int
    distance: int


def get_races():
    race_times = []
    race_distances = []
    with open(INPUT, 'r') as f_in:
        for raw_line in f_in:
            line = raw_line.strip()
            if line.startswith("Time"):
                _, times = line.split(":")
                race_times = [int(t) for t in re.findall(PATTERN, times)]
            if line.startswith("Distance"):
                _, distances = line.split(":")
                race_distances = [int(d) for d in re.findall(PATTERN, distances)]
            if race_times and race_distances:
                break
    assert len(race_times) == len(race_distances)

    return [Race(t,d) for t,d in zip(race_times, race_distances)]


def get_ways_to_win(race: Race) -> int:
    """For each whole millisecond you spend at the beginning of the race holding down the
    button, the boat's speed increases by one millimeter per millisecond."""

    # Solve t**2 - tT + D < 0
    # where t=charge time, T = total race time, D = best distance
    solutions = 0
    for t in range(race.time):
        answer = t**2 - (t*race.time) + race.distance
        if answer < 0:
            solutions += 1
            # print(f"Win with charge_time = {t} for race {race}")
    return solutions


def main1():
    races = get_races()
    total = 1

    for race in races:
        ways_to_win = get_ways_to_win(race)
        print(f"{ways_to_win} ways total to win for race {race}")
        total *= ways_to_win

    print(f"Total is {total}")


def main2():
    races = get_races()
    race_time_text = ''
    race_distance_text = ''
    for race in races:
        race_time_text += str(race.time)
        race_distance_text += str(race.distance)

    big_race = Race(time=int(race_time_text), distance=int(race_distance_text))
    ways_to_win = get_ways_to_win(big_race)
    print(f"Ways to win is {ways_to_win}")


if __name__ == "__main__":
    main2()
