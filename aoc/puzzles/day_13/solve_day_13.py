import copy
import os
from pathlib import Path
from pprint import pprint

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


@time_fn
def solve(day, sample, num_folds):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    coordinates_string, flip_commands = string_input.split('\n\n')
    print(coordinates_string)
    print(flip_commands)

    folds = []
    for line in flip_commands.split('\n'):
        print(line)
        print(line.split('='))
        axis, value = line.split('=')
        axis = axis[-1]

        print(axis, value)
        folds.append((axis,int(value)))

    print('coords')
    coordinates = []
    for coords in coordinates_string.split('\n'):
        print(coords)
        c,r = coords.split(',')
        coordinates.append((int(r),int(c)))
    H = max(map(lambda x: int(x[0]), coordinates)) + 1
    W = max(map(lambda x: int(x[1]), coordinates)) + 1
    print(H,'X',W)
    print(f"The answer is {answer}\n")


    mtx = [['.' for _ in range(W)] for __ in range(H)]


    for coord in coordinates:
        r,c = coord
        print(coord)
        mtx[r][c] = '#'
    # for row in mtx:
    #     print(row)

    # for h fold bottom half up
    # for y fold left half over

    folded_mtx = [['.' for _ in range(W+1)] for __ in range(H+1)]
    for fn, fold in enumerate(folds):
        if fn == num_folds:
            break
        axis, value  = fold
        new_bound = value
        if axis == 'y': # fold bottom up
            new_W = W
            new_H = H - new_bound
            print('old,new',H,W,new_H,new_W)
            # new_mtx =  [['.' for _ in range(W+1)] for __ in range(value, H+1)]

            # for r in mtx:
            #     print(r)
        else: # fold right half over left
            new_H = H
            new_W = W - new_bound
            # new_mtx =  [['.' for _ in range(value, W+1)] for __ in range(H+1)]
            # print(new_mtx)

        print('WXH',H,W)
        print(axis, value, new_H, new_W)
        print('flipping at ', axis,'=',value)
        print('before')
        # for ro in mtx:
        #     print(ro)
        # pprint(mtx)
        # print('after')
        for r in range(H):
            for c in range(W):
                cell = mtx[r][c]
                if r > value and axis == 'y':
                    if cell == '#':
                        mtx[value - abs(value - r)][c] = '#'
                    mtx[r][c] = 'X'
                elif c > value and axis == 'x':
                    if cell == '#':
                        mtx[r][value - abs(value - c)] = '#'
                    mtx[r][c] = 'X'
            # print(mtx[r])

    answer = 0
    for row in mtx:
        answer += sum(map(lambda x: 1 if x == '#' else 0, row))

    # pprint(mtx)

    str_rep = ""

    new_W = mtx[0].index('X')

    new_H = 99999
    for idx, row in enumerate(mtx):
        if row[0] == 'X' and idx < new_H:
            new_H = idx

    print(new_H, new_W)
    for row in mtx[:new_H]:
        r = row[:new_W]
        str_line = "".join(r)
        str_rep += '\n' + str_line
    print(str_rep)
    return answer

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    assert solve(_day_num, False, 1) == 607
    solve(_day_num, False, -1)  # letters are CPZLPFZL
    # solve(_day_num, sample=False)
