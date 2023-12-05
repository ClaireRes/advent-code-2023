import re


INPUT = "input4.txt"
TEST_INPUT = "testinput4.txt"
PATTERN = r"\s+(\d+)"


def get_winning_numbers_count(line: str) -> int:
    _, numbers = line.split(":", maxsplit=1)
    winners_text, actual_text = numbers.split("|", maxsplit=1)
    winners = {int(i) for i in re.findall(PATTERN, winners_text)}
    actual = [int(i) for i in re.findall(PATTERN, actual_text)]

    matching = [k for k in actual if k in winners]
    #print(f"Matched {matching} from line:\n{line}")
    return len(matching)


def main1():
    total = 0
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            winning_count = get_winning_numbers_count(line.strip())
            if winning_count > 0:
                total += 2**(winning_count - 1)

    print(f"Total = {total}")


def get_card_counts(original_winners: list) -> list:
    """
    Copies of scratchcards are scored like normal scratchcards and have the
     same card number as the card they copied. So, if you win a copy of card 10
      and it has 5 matching numbers, it would then win a copy of the same
      cards that the original card 10 won: cards 11, 12, 13, 14, and 15.
      This process repeats until none of the copies cause you to win any more cards.
       (Cards will never make you copy a card past the end of the table.)
    """
    card_count = [1 for _ in original_winners]
    for i, winners_count in enumerate(original_winners):
        # add copy to the winners_count cards after i
        # need to do this for the number of copies present for this card!
        #print(f"Adding copies for cards {i+1} - {i + winners_count} for Card {i}")
        copy_count = card_count[i]
        for k in range(i + 1, i + 1 + winners_count):
            card_count[k] += copy_count

    return card_count


def main2():
    original_winners = []
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            original_winners.append(get_winning_numbers_count(line.strip()))

    card_count = get_card_counts(original_winners)
    print(card_count)
    print(f"From {len(card_count)} cards got total cards + copies = {sum(card_count)}")


if __name__ == "__main__":
    main2()
