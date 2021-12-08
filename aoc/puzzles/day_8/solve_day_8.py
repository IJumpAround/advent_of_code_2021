import os
from collections import defaultdict
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

# 1 subset of: 0,3,4,7,8,9

# what we know so far (a,
# 1,4,7,8 - >

# A  7 - 1     gives us true segment a
#    7 & 1     gives (c/f) or (f/c)
#    4 - 7     gives (b/d) or (d/b)
#    8 - 7 - 4 gives (e/g) or (g/e)
#


# LET ZSN = 0 & 6 & 9 = {'a', 'b', 'f', 'g'} (known because they make up the numbers with 6 segments
# Let TTF = 2 & 3 & 5 = {'a','g','d'}  (known because they make up the numbers with 5 segments
# A = 7 - 1                                     'a'
# C = 4 - ZSN & 1 =                             'c'
# F = 1 - C   =                                 'f'
# TTF - 'a' - (4  - 7) =                        'g'
# TTF - 'g' = a,d - 'a' =                       'd'
# B = 4 - TTF - 1                               'b'
# E = (8 - 7) - B - A =                         'e'            {'a', 'b', 'c', 'd', 'e', 'f', 'g'}



# B =  (4 - 7) & ((2 U 3 U 5) - TTF - (7 & 1) = 'b'

# BE = 2 U 3 U 5 - TTF - (7 & 1) = {'b','e'}


# ZSN = (0 & 6 & 9) = {'a','b','d','e','f','g'}
# ZSN - {'a','b','d','e','g'} = 'f'
# 2,3,5 have same number of segments
# 2 & 3 & 5 = {'a','g','d'}
#
# b e are only present in one of the three
# From A we can find 3


# C  8 - 9 gives true segment e
# D  2 - 4 gives acdeg - bcdf = aeg -(A+C) = g
# E  2 - 0 gives acdeg - abcefg = d
# F  4 - 7 - E = (b/d) or (d/b) - d = b

# SEG = {
#     0: ['a','b','c','e','f','g'],
#     1: ['c', 'f'],
#     2: ['a',c'']
# }
SEG = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}

# key = number of segments, value = display number
LEN_SEG = defaultdict(list)

for k, v in SEG.items():
    LEN_SEG[v].append(k)
print('len seg', LEN_SEG)
print('num_segments->disp_number', LEN_SEG)


# wire -> seg


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    out_sum = 0
    list_input = input_loader.load_file_as_list(day, sample)
    # string_input = input_loader.load_file_as_string(day, sample)
    out_count = 0
    terminals = {}
    for line in list_input:
        wire_map = {
            'a': 'a',
            'b': 'b',
            'c': 'c',
            'd': 'd',
            'e': 'e',
            'f': 'f',
            'g': 'g'
        }

        digit_to_pattern = {}
        pattern_to_digit = {}
        sig_input, output = line.split('|')
        sig_input = sig_input.strip()
        output = output.strip()

        print(line)
        patterns = sig_input.split()
        for pattern in patterns:

            if len(LEN_SEG[len(pattern)]) == 1:
                digit = LEN_SEG[len(pattern)][0]
                # terminals[digit] = len(pattern)
                digit_to_pattern[digit] = set(pattern)
                pattern_to_digit["".join(sorted(pattern))] = digit

        # print('terminals (digit->num_segments)', terminals)
        # print(sig_input, output)
        print('pattern->number', pattern_to_digit)
        print('number->abcd: ',digit_to_pattern)
        ONE = digit_to_pattern[1]
        FOUR = digit_to_pattern[4]
        print(f'{FOUR=}')
        SEVEN = digit_to_pattern[7]
        EIGHT = digit_to_pattern[8]

        ZSN =  reduce(lambda x, y:  x & y ,[set(pattern) for pattern in patterns if len(pattern) == 6])
        TTF =  reduce(lambda x, y:  x & y ,[set(pattern) for pattern in patterns if len(pattern) == 5])

        print('ZSN: ',ZSN)
        print('TTF: ',TTF)
        A = SEVEN - ONE
        B = FOUR - TTF - ONE
        C = FOUR - ZSN & ONE
        G = TTF - A - (FOUR - SEVEN)
        D = TTF - G - A
        E = (EIGHT - ZSN - FOUR)
        F = ONE - C
        print(f'{A=}')
        print(f'{B=}')
        print(f'{C=}')
        print(f'{D=}')
        print(f'{E=}')
        print(f'{F=}')
        print(f'{G=}')

        ZERO = "".join(sorted(A | B | C | E | F | G))
        ONE = "".join(sorted(ONE))
        TWO = "".join(sorted(A |  C | D | E | G))
        THREE = "".join(sorted(A | C | D | F | G))
        FOUR = "".join(sorted(FOUR))
        FIVE  = "".join(sorted(A | B | D | F | G))
        SIX  = "".join(sorted(A | B | D | E | F | G))
        SEVEN  = "".join(sorted(SEVEN))
        EIGHT  = "".join(sorted(EIGHT))
        NINE  = "".join(sorted(A | B | C | D |  F | G))

        wire_map[A.pop()] = 'a'
        wire_map[B.pop()] = 'b'
        wire_map[C.pop()] = 'c'
        wire_map[D.pop()] = 'd'
        wire_map[E.pop()] = 'e'
        wire_map[F.pop()] = 'f'
        wire_map[G.pop()] = 'g'

        for k in wire_map:
            assert len(k) == 1


        print('wires :', wire_map)


        print(f'{ZERO=}')
        print(f'{ONE=}')
        print(f'{TWO=}')
        print(f'{THREE=}')
        print(f'{FOUR=}')
        print(f'{FIVE=}')
        print(f'{SIX=}')
        print(f'{SEVEN=}')
        print(f'{EIGHT=}')
        print(f'{NINE=}')
        # C = FOUR -

        print()

        out_values = output.split()


        number = ""
        number_map = {
            ZERO: 0,
            ONE: 1,
            TWO: 2,
            THREE: 3,
            FOUR: 4,
            FIVE: 5,
            SIX: 6,
            SEVEN: 7,
            EIGHT: 8,
            NINE: 9,
        }
        new_number_map = number_map
        print(f'{number_map=}')
        # number_map = {wire_map[wire]: value for wire, value in [pattern for pattern in number_map.items()]}
        # for pattern, v in list(number_map.items()):
        #     new_pattern = "".join(sorted([wire_map[letter] for letter in pattern]))
        #     # del number_map[pattern]
        #     new_number_map[new_pattern] = v


        print(f'{new_number_map=}')
        for o in out_values:
            number += str(new_number_map["".join(sorted(o))])
            if "".join(sorted(o)) in pattern_to_digit:
                out_count += 1
        print('number ', number)
        out_sum += int(number)

    answer = out_count
    print(f"1 4 7 8 count: ", answer)
    print(f"sum of out values: ", out_sum)
    # print(digit_to_pattern)
    return answer

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    # solve(_day_num, sample=False)
    solve(_day_num, sample=False)
