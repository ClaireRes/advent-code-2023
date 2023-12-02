import re
from typing import NamedTuple

INPUT = "input2.txt"
MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14
PATTERN = r"Game (?P<id>\d+):"

RED_PATTERN = r".*\s(\d+) red"
GREEN_PATTERN = r".*?\s(\d+) green"
BLUE_PATTERN = r".*?\s(\d+) blue"


class Round(NamedTuple):
    red: int
    green: int
    blue: int


class Game(NamedTuple):
    game_id: int
    rounds: list[Round]


def get_colour_number(pattern: str, text: str) -> int:
    c_match = re.match(pattern, text)
    if c_match:
        num = int(c_match.group(1))
    else:
        num = 0
    return num


def process_line(line: str) -> Game:
    match = re.match(PATTERN, line)
    game_id = int(match.group("id"))

    _game, rounds_full_text = line.split(':', maxsplit=1)
    rounds_text = rounds_full_text.split(';')

    rounds = []
    for round_text in rounds_text:
        red = get_colour_number(RED_PATTERN, round_text)
        green = get_colour_number(GREEN_PATTERN, round_text)
        blue = get_colour_number(BLUE_PATTERN, round_text)
        rounds.append(Round(red, green, blue))

    return Game(game_id, rounds)


"""
PART 1:
Determine which games would have been possible if the bag had been loaded 
with only 12 red cubes, 13 green cubes, and 14 blue cubes.
What is the sum of the IDs of those games?
"""


def is_possible(game: Game) -> bool:
    for game_round in game.rounds:
        if game_round.red > MAX_RED or game_round.green > MAX_GREEN or game_round.blue > MAX_BLUE:
            return False
    return True


"""
PART 2:
For each game, find the minimum set of cubes that must have been present.
What is the sum of the power of these sets?
"""


def get_cube_power(game: Game) -> int:
    # Min num required for each colour is largest we see for that colour
    red_max = 0
    green_max = 0
    blue_max = 0
    for g_round in game.rounds:
        red_max = max(red_max, g_round.red)
        green_max = max(green_max, g_round.green)
        blue_max = max(blue_max, g_round.blue)

    print(game)
    print(f"r: {red_max}, g: {green_max}, b: {blue_max}")
    return red_max * green_max * blue_max


def main2():
    cube_powers = []
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            game = process_line(line.strip())
            cube_powers.append(get_cube_power(game))

    print(f"Sum of cube powers = {sum(cube_powers)}")


def main1():
    # Example input
    # Game 73: 7 green, 6 red, 7 blue; 6 blue, 5 red, 8 green; 5 blue, 5 red
    possible = []
    num_games = 0
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            num_games += 1
            game = process_line(line.strip())
            game_possible = is_possible(game)
            if game_possible:
                possible.append(game.game_id)

            print(f"{game_possible} -> {game}")
            print(line)

    print(f'total possible games = {len(possible)}/{num_games}')
    print(f"Total is {sum(possible)}")


if __name__ == "__main__":
    main2()
