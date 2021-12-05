import os
from pathlib import Path

from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE

os.environ['LOG_LEVEL'] = 'DEBUG'
from aoc import logger
from aoc.utils import input_loader
#
#
# def bounds(coords):
#
#     for coord in coords:



def solve(day, sample, diag=True):
    logger.info(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)


    coords_l = []
    coords_r = []
    for line in list_input:
        coordl, coordr = line.split('->')

        coordl = tuple(map(int,coordl.strip().split(',')))
        coordr = tuple(map(int,coordr.strip().split(',')))
        coords_l.append(coordl)
        coords_r.append(coordr)

    logger.info(coords_r)
    logger.info(coords_l)


    vertical_lines = []
    horizontal_lines = []
    diagonal_lines = []
    maxy,miny,maxx,minx = None, None, None,None
    for left,right in zip(coords_l, coords_r):
        if left[0] == right[0]:
            vertical_lines.append((left, right))
        elif left[1] == right[1]:
            horizontal_lines.append((left, right))
        else:
            diagonal_lines.append((left,right))

        for pt in [left, right]:
            if not maxx or pt[0] > maxx[0]:
                maxx = pt
            elif not maxy or pt[1] > maxy[1]:
                maxy = pt
            elif not minx or pt[0] < minx[0]:
                minx = pt
            elif not miny or pt[1] < miny[1]:
                miny = pt



    h_bounds = minx[0] + maxx[0] + 1
    v_bounds = maxy[1] + miny[1] + 1

    # logger.info(str(h_bounds), str(v_bounds))
    print(h_bounds)
    print(v_bounds)

    import numpy as np

    board = np.zeros((h_bounds, v_bounds))

    for line in horizontal_lines:
        l, r = line
        l, r = sort_pair(l, r)
        board[l[1], l[0]:r[0]+1] += 1

    for line in vertical_lines:
        l, r = line
        l, r = sort_pair(l, r, False)
        board[l[1]:r[1] + 1, l[0]] += 1
    logger.info(f'\n{board}')

    if diag:
        for line in diagonal_lines:
            l, r = line
            points = gen_diag_points(l, r)
            logger.info(f'Starting points: {l,r}')
            logger.info(f'Generated: {points}')
            for pt in points:
                board[pt[1]][pt[0]] += 1


    logger.info(f'\n{board}')

    total = np.count_nonzero(board > 1)

    logger.info(f'Overlapping points: {total}')

    return total


def gen_diag_points(l, r):
    l, r = sort_pair(l, r)

    new_points = []
    slope = (r[1] - l[1])/(r[0] - l[0])

    for i in range(l[0] + 1, r[0]):
        new_points.append((i, int(slope * (i - l[0])) + l[1]))

    new_points.insert(0, l)
    new_points.append(r)
    return new_points


def sort_pair(l, r, horiz=True):
    if horiz:
        if l[0] > r[0]:
            return r, l
    else:
        if l[1] > r[1]:
            return r, l

    return l, r



if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    assert solve(_day_num, sample=False, diag=False) == 7674
    assert solve(_day_num, sample=False) == 20898
