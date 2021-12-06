import os
from pathlib import Path
from pprint import pprint

from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

os.environ['LOG_LEVEL'] = 'DISABLED'
from aoc import logger
from aoc.utils import input_loader


def sum_unmarked(board) -> int:
    total = 0
    for row in board:
        total += sum([int(val) for val in row if val != 'x'])

    return total


def mark_board(board, value):
    value = int(value)
    for row in range(len(board)):
        for col, val in enumerate(board[row]):
            if val != 'x' and val == value:
                board[row][col] = 'x'


def mark_boards(boards, value):
    for board in boards:
        mark_board(board, value)


def check_boards(boards):
    winners = []
    for board in boards:
        result = check_board(board)
        if result:
            winners.append(result)
    return winners


def check_board(board):
    for row in board:
        try:
            r = "".join(row)
        except:
            continue
        else:
            return board

    for x in range(len(board)):
        col = []
        for y in range(len(board[x])):
            col.append(board[y][x])

        try:
            r = "".join(col)
        except:
            continue
        else:
            return board

@time_fn
def solve(day, sample):
    logger.info(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample, line_as_list=True)

    draw_order = list_input.pop(0)
    draw_order = draw_order[0].split(',')
    list_input.pop(0)

    boards = []
    board = []
    for row in list_input:
        if len(row) != 0:
            row = list(map(int, row))
            board.append(row)

        if len(row) == 0 and board:
            boards.append(board)
            board = []
    boards.append(board)
    for board in boards:
        pprint(board)
    print('draw: ', draw_order)

    num_boards = len(boards)
    winner = None
    last_called = None
    winner_count = 0
    last_winner = None
    for number in draw_order:
        last_called = number
        mark_boards(boards, number)
        winners = check_boards(boards)
        if winners:
            winner = winners[-1]
            winner_count += len(winners)
            for winner in winners:
                boards.remove(winner)
            # winner = winners[0]
            last_winner = winner
            winner = None

            if winner_count == num_boards:
                break
            pass

    winner = last_winner

    print("LAST NUMBER: ", last_called)
    print("WINNER:")
    pprint(winner)

    unmarked = sum_unmarked(winner)
    last_called = int(last_called)

    print('unmarked ', unmarked)
    print('last called ', last_called)
    answer = unmarked * last_called
    print(f"The answer is {answer}\n")

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    # solve(_day_num, sample=False)
    assert solve(_day_num, sample=False) == 13912
