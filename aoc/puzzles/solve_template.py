import os

os.environ['LOG_LEVEL'] = 'INFO'
from aoc import logger
from aoc.utils import input_loader


def solve(day, sample):
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    logger.info(f"The answer is {answer}")


if __name__ == '__main__':
    _day_num = int(__name__.split('_')[-1])
    solve(_day_num, sample=False)
    solve(_day_num, sample=True)
