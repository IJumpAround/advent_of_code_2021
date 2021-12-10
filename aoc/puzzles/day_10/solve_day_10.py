import os
from pathlib import Path

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger

# chunks have 0 or more sub chunks
# adjacent chunks not delimited

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
# @time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    print(f"The answer is {answer}\n")

    # push until close symbol
    # pop until correct open symbol
    #   push any other encountered onto another stack
    #   when 1st symbol found


    score = 0
    fixer_scores = []
    scorers = []

    for i, line in enumerate(list_input):
        encountered = []
        fixers = []
        incomplete = True
        for j, symb in enumerate(line):
            # print(encountered)
            if symb in SCORE:
                # print('end', symb)
                last = encountered.pop()
                last_closer = symb
                if not ord(symb) == (ord(last) + (1 if symb == ')' else 2)):
                    scorers.append((i, j, last_closer))
                    # print('closer ', last_closer)
                    score += SCORE[last_closer]
                    # print('scored: ', SCORE[last_closer])
                    incomplete = False
                    break
            else:
                encountered.append(symb)

        if incomplete:
            fixer_score = 0
            while encountered:
                nxt = encountered.pop()
                fixer = chr(ord(nxt) + (1 if nxt == '(' else 2))
                fixers.append(fixer)

                fixer_score *= 5
                fixer_score += CLOSER_SCORE[fixer]
            fixer_scores.append(fixer_score)

    answer = score

    print('score ', score)
    print(f'{scorers=}')
    # print(fixers)
    fixer_scores = sorted(fixer_scores)
    print('Fixer score: ', fixer_scores)
    winning_fixer = sorted(fixer_scores)[len(fixer_scores)//2]
    print('winner fixer', winning_fixer)

    assert score == 339537
    assert winning_fixer == 2412013412
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    # solve(_day_num, sample=True)
    solve(_day_num, sample=False)
