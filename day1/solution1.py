import string


INPUT = "input1.txt"
DIGITS = [d for d in string.digits]
WORDS_TO_DIGITS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def build_prefix_tree() -> dict:
    prefix_tree = dict()
    current_dict = prefix_tree
    for word in WORDS_TO_DIGITS.keys():
        for letter in word:
            if letter not in current_dict:
                next_dict = dict()
                current_dict[letter] = next_dict
                current_dict = next_dict
            else:
                current_dict = current_dict[letter]

        # reset to top level dict
        current_dict = prefix_tree
    print(prefix_tree)
    return prefix_tree


PREFIX_TREE = build_prefix_tree()


def get_number_from_value_part1(value: str) -> int:
    first_digit_char = ''
    last_digit_char = ''

    for c in value:
        if c in DIGITS:
            # only update first digit pointer if this is the first digit
            if not first_digit_char:
                first_digit_char = c
            last_digit_char = c

    if not first_digit_char:
        number = 0
    else:
        number = int(first_digit_char + last_digit_char)
    print(f'Mapped "{value}" -> {number}')
    return number


def get_first_digit(value: str, first_digit_idx: int, first_word_idx: int, first_word_digit: str) -> str:
    if first_digit_idx < 0:
        first_digit = first_word_digit
    elif first_word_idx < 0 or (first_digit_idx < first_word_idx):
        first_digit = value[first_digit_idx]
    else:
        first_digit = first_word_digit
    return first_digit


def get_last_digit(value: str, last_digit_idx: int, last_word_idx: int, last_word_digit: str) -> str:
    if last_digit_idx < 0:
        last_digit = last_word_digit
    elif last_word_idx < 0 or last_digit_idx > last_word_idx:
        last_digit = value[last_digit_idx]
    else:
        last_digit = last_word_digit
    return last_digit


def get_number_from_value_part2(value: str) -> int:
    first_digit_idx = -1
    last_digit_idx = -1
    first_word_idx = -1
    last_word_idx = -1
    first_word_digit = ''
    last_word_digit = ''

    i = 0
    while i < len(value):
        current_char = value[i]
        if current_char in DIGITS:
            # only update first digit pointer if this is the first digit
            if first_digit_idx < 0:
                first_digit_idx = i
            last_digit_idx = i
            i += 1
        elif i < len(value) - 1:
            # Traverse prefix tree starting from the current letter
            # Use lookahead to make sure we don't miss a number from edge case like 'fone'
            current_dict = PREFIX_TREE
            start_substr = i
            if current_char not in current_dict:
                i += 1
            else:
                substr = current_char
                current_dict = current_dict.get(current_char)
                while i < (len(value) - 1) and value[i+1] in current_dict:
                    substr += value[i + 1]
                    current_dict = current_dict.get(value[i + 1])
                    # stop if we found a valid word to handle a case like 'eightwo'
                    if substr in WORDS_TO_DIGITS:
                        break
                    i += 1

                if substr in WORDS_TO_DIGITS:
                    word_as_digit = WORDS_TO_DIGITS.get(substr)
                    if first_word_idx < 0:
                        first_word_idx = start_substr
                        first_word_digit = word_as_digit
                    last_word_idx = start_substr
                    last_word_digit = word_as_digit
                # don't get stuck on same char if we didn't find a >1 length prefix
                elif len(substr) == 1:
                    i += 1
        else:
            i += 1

    first_digit = get_first_digit(value, first_digit_idx, first_word_idx, first_word_digit)
    last_digit = get_last_digit(value, last_digit_idx, last_word_idx, last_word_digit)

    number = int(first_digit + last_digit)
    print(f'Mapped "{value}" -> {number}')
    return number


def main():
    total = 0
    with open(INPUT, 'r') as f_in:
        for line in f_in:
            number = get_number_from_value_part2(line.strip().lower())
            total += number

    print(f"Total is {total}")


if __name__ == "__main__":
    main()
