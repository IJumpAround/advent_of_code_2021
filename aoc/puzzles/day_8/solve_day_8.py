import os
from functools import reduce
from pathlib import Path

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg


# Algorithm: define ahead of time a series of set operations that will eliminate unknowns and
# reduce to the encoded representation of each particular letter.
# Once we've solved for each letter representation we can map the input and output patterns
# onto the numbers they represent.
#
# We know which patterns represent each of 1,4,7,8 because they each have a unique number of segments.
# We don't know 0,6,9 or 2,3,5 individually, but we know their lengths.
# 0,6,9 all have  6 segments
# 2,3,5 all have 5 segments
# We can use this knowledge to operate on their intersection and isolate other segments.

# The following set operations will yield the encoded version of the true segment value
# LET ZSN = {0 & 6 & 9} = {a, b, f, g}     (known because they make up the numbers with 6 segments)
# Let TTF = {2 & 3 & 5} = {a, g, d}        (known because they make up the numbers with 5 segments)
# A = 7 - 1
# C = 4 - ZSN & 1
# F = 1 - c
# G = TTF - a - (4  - 7)
# D = TTF - g - a
# B = 4 - TTF - 1
# E = 8 - ZSN - 4


# map the length of patterns to their digit equivalent for pre-known values
KNOWN_DIGITS = {
    2: 1,
    4: 4,
    3: 7,
    7: 8
}


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")

    list_input = input_loader.load_file_as_list(day, sample)
    out_sum = 0
    out_count = 0

    for line in list_input:
        sig_input, output = line.split('|')
        out_values = output.split()
        print(line)

        patterns = sig_input.split()
        patterns_as_sets = [set(pattern) for pattern in patterns]  # since we turn patterns into sets several times
        digit_to_pattern = {KNOWN_DIGITS[len(pattern)]: pattern for pattern in patterns_as_sets if
                            len(pattern) in KNOWN_DIGITS}

        ONE = digit_to_pattern[1]
        FOUR = digit_to_pattern[4]
        SEVEN = digit_to_pattern[7]
        EIGHT = digit_to_pattern[8]
        ZSN = reduce(lambda x, y: x & y, [pattern for pattern in patterns_as_sets if len(pattern) == 6])  # {0 & 6 & 9}
        TTF = reduce(lambda x, y: x & y, [pattern for pattern in patterns_as_sets if len(pattern) == 5])  # {2 & 3 & 5}


        # Do some set math to confirm letters
        A = SEVEN - ONE
        B = FOUR - TTF - ONE
        C = FOUR - ZSN & ONE
        G = TTF - A - (FOUR - SEVEN)
        D = TTF - G - A
        E = (EIGHT - ZSN - FOUR)
        F = ONE - C

        number_map = {
            "".join(sorted(A | B | C | E | F | G)): 0,   # ZERO
            "".join(sorted(ONE)):                   1,   # ONE
            "".join(sorted(A | C | D | E | G)):     2,   # TWO
            "".join(sorted(A | C | D | F | G)):     3,   # THREE
            "".join(sorted(FOUR)):                  4,   # FOUR
            "".join(sorted(A | B | D | F | G)):     5,   # FIVE
            "".join(sorted(A | B | D | E | F | G)): 6,   # SIX
            "".join(sorted(SEVEN)):                 7,   # SEVEN
            "".join(sorted(EIGHT)):                 8,   # EIGHT
            "".join(sorted(A | B | C | D | F | G)): 9,   # NINE
        }

        print(f'{number_map=}')
        number = ""
        for o in out_values:
            # build up the encoded number piece by piece
            actual_number = number_map["".join(sorted(o))]
            number += str(actual_number)

            # p1 answer counts the number of times the terminals appear in the output
            if actual_number in [1, 4, 7, 8]:
                out_count += 1

        print('decoded number ', number)
        out_sum += int(number)
        print()

    answer = out_count
    print(f"1 4 7 8 count: ", answer)
    print(f"sum of out values: ", out_sum)

    return out_count, out_sum


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    assert solve(_day_num, False)[0] == 321
    assert solve(_day_num, False)[1] == 1028926
