from collections import Counter, defaultdict
from enum import Enum
from typing import NamedTuple, List


INPUT = "input7.txt"
TEST_INPUT = "testinput7.txt"
CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARD_RANKS = dict(zip(CARDS, reversed(range(len(CARDS)))))

CARDS_2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
CARD_RANKS_2 = dict(zip(CARDS_2, reversed(range(len(CARDS_2)))))

JOKER = "J"


class HandType(Enum):
    FIVE_OK = 6
    FOUR_OK = 5
    FULL_HOUSE = 4
    THREE_OK = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


class Hand(NamedTuple):
    cards: str
    bid: int


def get_hand_type(hands: Hand) -> HandType:
    counts = Counter(hands.cards)
    max_count = max(counts.values())
    unique = len(counts)
    
    if unique == 1:
        return HandType.FIVE_OK
    if unique == 2:
        # either 2+3 or 4+1
        if max_count == 4:
            return HandType.FOUR_OK
        return HandType.FULL_HOUSE
    if unique == 3:
        # either 3+1+1 or 2+2+1
        if max_count == 3:
            return HandType.THREE_OK
        return HandType.TWO_PAIR
    if unique == 4:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


def get_hand_type_with_jokers(hands: Hand) -> HandType:
    counts = Counter(hands.cards)
    max_count = max(counts.values())
    unique = len(counts)

    if unique == 1:
        return HandType.FIVE_OK
    if unique == 2:
        # (4, 1) or (2, 3)
        # with joker, either (4*, 1) -> 5 or (4, 1*) -> 5, or (2*, 3) -> 5 or (2, 3*) -> 5
        if JOKER in counts:
            return HandType.FIVE_OK
        if max_count == 4:
            return HandType.FOUR_OK
        return HandType.FULL_HOUSE
    if unique == 3:
        # (3, 1, 1) or (2, 2, 1)
        if max_count == 3:
            # (3*, 1, 1) -> 4, 1 or (3, 1*, 1) -> (4, 1)
            if JOKER in counts:
                return HandType.FOUR_OK
            return HandType.THREE_OK
        if JOKER in counts:
            # (2*, 2, 1) -> (4, 1) or (2, 2, 1*) -> (3, 2)
            if counts[JOKER] == 2:
                return HandType.FOUR_OK
            return HandType.FULL_HOUSE
        return HandType.TWO_PAIR
    if unique == 4:
        # (*2, 1, 1, 1) -> (3, 1, 1) or (2, 1, 1, *1) -> (3, 1, 1)
        if JOKER in counts:
            return HandType.THREE_OK
        return HandType.ONE_PAIR

    if JOKER in counts:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


def rank_hands(hands: List[Hand], card_ranks: dict):
    # rank based on first card, then second on tie, then third etc.
    hands.sort(key=lambda h: tuple(card_ranks[i] for i in h.cards))


def main1():
    # orders hands in increasing strength
    hands_by_type_rank = [[] for _ in HandType]

    num_hands = 0
    with open(TEST_INPUT, 'r') as f_in:
        for line in f_in:
            cards, bid_text = line.strip().split(" ", maxsplit=1)
            hand = Hand(cards, int(bid_text))
            hand_type = get_hand_type(hand)
            hands_by_type_rank[hand_type.value].append(hand)
            num_hands += 1

    total = 0
    rank = 1
    for hands_list in hands_by_type_rank:
        rank_hands(hands_list, CARD_RANKS)
        for hand in hands_list:
            total += (rank * hand.bid)
            rank += 1

    print(f"Total is {total}")


def main2():
    # orders hands in increasing strength
    hands_by_type_rank = [[] for _ in HandType]

    num_hands = 0
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            cards, bid_text = line.strip().split(" ", maxsplit=1)
            hand = Hand(cards, int(bid_text))
            hand_type = get_hand_type_with_jokers(hand)
            print(f"Hand: {hand}, type: {hand_type.name}")
            hands_by_type_rank[hand_type.value].append(hand)
            num_hands += 1

    total = 0
    rank = 1
    for hands_list in hands_by_type_rank:
        rank_hands(hands_list, CARD_RANKS_2)
        for hand in hands_list:
            total += (rank * hand.bid)
            rank += 1

    print(f"Total is {total}")


if __name__ == "__main__":
    main2()
