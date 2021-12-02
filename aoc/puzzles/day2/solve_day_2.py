import os

os.environ['LOG_LEVEL'] = 'DEBUG'
from aoc import logger
from aoc.utils import input_loader


def solve(day):
    lines = input_loader.load_file_as_list(day)
    posx = 0
    posy = 0
    aim = 0

    for line in lines:
        cmd, amt = line.split()
        amt = int(amt)

        if cmd == 'forward':
            posx += amt
            posy += aim * amt
        else:
            aim += amt * (1 if cmd == 'down' else -1)

    logger.info(f"Final pos {posx},{posy}")

    logger.info(f"Answer: {final(posx, posy)}")


def final(x, y):
    return x * y





if __name__ == '__main__':
    solve(2)