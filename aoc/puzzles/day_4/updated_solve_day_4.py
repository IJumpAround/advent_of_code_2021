import os
os.environ['LOG_LEVEL'] = 'INFO'
import time
from pathlib import Path
from pprint import pformat

from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader
import numpy as np


def mark_boards(boards, value):
    for board in boards:
        board[board == value] = -1


def check_boards(boards):
    winners = []
    for board in boards:
        result = check_board_for_win(board)
        if result is not None:
            winners.append(result)

    return winners


def check_board_for_win(board: np.array):
    board_mask = board == -1
    for axis in [0, 1]:
        if board_mask.all(axis=axis).any():
            return board


def remove_winner(boards, winner):
    ind = 0
    size = len(boards)
    while ind != size and not np.array_equal(boards[ind], winner):
        ind += 1
    if ind != size:
        boards.pop(ind)
    else:
        raise ValueError('array not found in list.')


@time_fn
def solve(day, sample, part=2):
    logger.info(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")

    list_input = input_loader.load_file_as_list(day, sample)

    draw_order = [int(i) for i in list_input.pop(0).split(',')]
    list_input.pop(0)  # remove leading newline/space

    boards = "\n".join(list_input).split('\n\n')  # group each board as a string entry in a list

    def make_board(board_lines):
        return np.array([list(map(lambda ch: int(ch.strip()), line.strip().split())) for line in board_lines])

    # result is list of boards, where each board is an ndarray
    boards = [make_board(board_arr) for board_arr in [board.split('\n') for board in boards]]

    for board in boards:
        logger.debug(pformat(board))
    logger.info(f'draw order: {draw_order}')

    og_boards = boards[:]
    winners = []
    for number in draw_order:
        mark_boards(boards, number)
        round_winners = check_boards(boards)

        for winner in round_winners:
            winners.append((winner, number))
            remove_winner(boards, winner)

        # all boards have completed
        if len(winners) == len(og_boards):
            break

    if part == 2:
        answer = p2_answer(*winners[-1])
    else:
        answer = p1_answer(*winners[0])

    return answer


def p1_answer(winner, winning_number):
    answer = np.sum(winner[winner != -1])
    answer *= winning_number

    logger.info(f"{winner}")
    logger.info(f'Winner on number: {winning_number}')
    return answer


def p2_answer(winner, last_called):
    unmarked = np.sum(winner[winner != -1])
    answer = unmarked * last_called

    logger.info(f'last called {last_called}')
    logger.info(f"The answer is {answer}\n")
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    s = time.time()
    p1_sample_ans = solve(_day_num, sample=True, part=1)
    p1_ans = solve(_day_num, sample=False, part=1)
    res1 = solve(_day_num, sample=True)
    res2 = solve(_day_num, sample=False)

    assert p1_sample_ans == 4512
    assert p1_ans == 72770
    assert res1 == 1924
    assert res2 == 13912

    logger.info(f'Time to run all tests: {time.time() -s}s')