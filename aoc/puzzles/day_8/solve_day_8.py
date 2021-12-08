import os
from collections import defaultdict
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

for k,v in SEG.items():
    LEN_SEG[v].append(k)
print('num_segments->disp_number', LEN_SEG)


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    # string_input = input_loader.load_file_as_string(day, sample)
    out_count = 0
    terminals = {}
    for line in list_input:
        digit_to_pattern = {}
        pattern_to_digit = {}
        sig_input, output = line.split('|')
        sig_input = sig_input.strip()
        output = output.strip()

        patterns = sig_input.split()
        for pattern in patterns:

            if len(LEN_SEG[len(pattern)]) == 1:
                digit = LEN_SEG[len(pattern)][0]
                terminals[digit] = len(pattern)
                digit_to_pattern[digit] = pattern
                pattern_to_digit["".join(sorted(pattern))] = digit

        print('terminals (digit->num_segments)', terminals)
        print(sig_input, output)
        print('p->d', pattern_to_digit)


        out_values = output.split()


        for o in out_values:
            print(o)
            if "".join(sorted(o)) in pattern_to_digit:
                out_count += 1


    answer = out_count
    print(f"The answer is {answer}\n")
    print(digit_to_pattern)
    return answer

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    # solve(_day_num, sample=False)
    solve(_day_num, sample=False)
