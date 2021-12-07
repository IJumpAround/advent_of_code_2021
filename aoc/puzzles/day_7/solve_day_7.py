import os
from collections import defaultdict
from pathlib import Path

from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

os.environ['LOG_LEVEL'] = 'INFO'
from aoc import logger
from aoc.utils import input_loader

L = logger


@time_fn
def solve(day, sample):
    C = defaultdict(int)
    L.info(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    # list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)
    L.info(string_input)

    crab_subs = [int(c) for c in string_input.split(',')]
    for c in crab_subs:
        C[c] += 1

    # Cost = {i:0 for i in range(min(C), min(C) + max(C))}
    # cost =
    # Cost = defaultdict(int)
    Cost = [0 for _ in range(min(C), min(C) + max(C))]

    print(Cost)
    for i, h in enumerate(Cost):
        for j in C:
            # end_range = abs(i - j)
            Cost[i] += sum(range(0, abs(j-i)+1)) * C[j]

    L.info(f'cost {Cost}')
    # L.info(f"The answer is {answer}\n")
    cost = min(Cost)
    pos = Cost.index(cost)

    answer = pos
    print(answer,cost)
    return answer

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    # solve(_day_num, sample=True)
    solve(_day_num, sample=False)
