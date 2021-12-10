import os
from pathlib import Path


os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.measurement import time_fn
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE

from aoc import logger
from aoc.utils import input_loader

L = logger

SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

CLOSER_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")

    list_input = input_loader.load_file_as_list(day, sample)

    score = 0
    fixer_scores = []

    for i, line in enumerate(list_input):
        encountered = []
        incomplete = True
        for j, symb in enumerate(line):
            if symb in SCORE:
                last = encountered.pop()
                last_closer = symb
                if not ord(symb) == (ord(last) + (1 if symb == ')' else 2)):
                    score += SCORE[last_closer]
                    incomplete = False
                    break
            else:
                encountered.append(symb)

        if incomplete:
            fixer_score = 0
            while encountered:
                nxt = encountered.pop()
                fixer = chr(ord(nxt) + (1 if nxt == '(' else 2))

                fixer_score = (fixer_score * 5) + CLOSER_SCORE[fixer]
            fixer_scores.append(fixer_score)

    winning_fixer = sorted(fixer_scores)[len(fixer_scores)//2]
    print('Syntax error score ', score)
    print('Fixer score', winning_fixer)

    assert score == 339537
    assert winning_fixer == 2412013412


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=False)
