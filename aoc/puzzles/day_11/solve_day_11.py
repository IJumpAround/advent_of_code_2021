import os
from pathlib import Path

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


def in_bounds(coords, H, W):
    r,c = coords
    return 0 <= r < H and 0 <= c < W


def adjacent_coords(origin: tuple):
    adjacent = []
    for i in range(origin[0]-1, origin[0]+2):
        for j in range(origin[1]-1, origin[1]+2):
            if (i, j) != origin:
                adjacent.append((i, j))

    return adjacent


def flash(board, flashed,  coords):
    H = len(board)
    W = len(board[0])

    if not in_bounds(coords, H, W):
        return

    r, c = coords[0], coords[1]
    flashed[r][c] = True
    adjacent = adjacent_coords((r, c))

    for adj in adjacent:
        ar, ac = adj

        if not in_bounds((ar,ac), H, W):
            continue

        board[ar][ac] += 1
        if not flashed[ar][ac] and board[ar][ac] > 9:
            flash(board, flashed, (ar,ac))


def pboard(board):
    for row in board:
        print(row)


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")

    list_input = input_loader.load_file_as_list(day, sample)
    flash_count = 0
    octo_board = []
    sync_step = -1
    for row in list_input:
        new_row = [int(octo) for octo in row]
        print(new_row)
        octo_board.append(new_row)

    stop_flash_count_step = 100
    step = 0
    while sync_step == -1:

        flashed_this_step = [[0 for __ in range(len(octo_board))] for _ in range(len(octo_board[0]))]
        # Phase 1 increment each octopus brightness
        for row in range(len(octo_board)):
            for col in range(len(octo_board[row])):
                octo_board[row][col] += 1

        # Phase 2 run chain flashes
        for row in range(len(octo_board)):
            for col in range(len(octo_board[row])):
                if octo_board[row][col] > 9 and not flashed_this_step[row][col]:
                    flash(octo_board, flashed_this_step, (row, col))

        flashes_this_step = 0
        # Phase 3 reset brightnesses above 9 to 0
        for i, r in enumerate(flashed_this_step):
            for j, c in enumerate(flashed_this_step[i]):
                if step < stop_flash_count_step:
                    flash_count += c
                flashes_this_step += c
                if c is True:
                    octo_board[i][j] = 0
        if flashes_this_step == len(octo_board) * len(octo_board[0]) and sync_step == -1:
            sync_step = step
        step += 1

        print()
        pboard(octo_board)

    answer = flash_count
    print(f"The answer is {answer}\n")
    print(f"Synchronized step was on step {sync_step+1}")

    if sample:
        assert answer == 1656
        assert sync_step + 1 == 195
    else:
        assert answer == 1785
        assert sync_step + 1 == 354
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=False)
