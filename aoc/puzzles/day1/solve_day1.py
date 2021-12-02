import os

os.environ['LOG_LEVEL'] = 'INFO'
from aoc import logger
from aoc.utils import input_loader


def solve(sample=False, window_size=1):
    file = 'input.txt' if not sample else 'sample.txt'
    depth_list = list(map(int, input_loader.load_file_as_newlines('day1', filename=file)))

    depth_increases = count_increases(depth_list, window_size)

    logger.info(f"{depth_increases} Increases with window size: {window_size}")


def count_increases(depth_list: list[int], window_size):
    count = 0
    last = depth_list[:window_size:1]
    logger.debug("Window size: %s" % window_size)
    for i in range(window_size + 1, len(depth_list) + 1):
        start = i - window_size
        window = depth_list[start: start + window_size]
        cur_sum = sum(window)
        pre_sum = sum(last)

        if cur_sum > pre_sum:
            count += 1
        logger.debug(f'{last} {window} {pre_sum} < {cur_sum} = {pre_sum<cur_sum}')
        last = window

    return count


if __name__ == '__main__':

    solve(sample=False, window_size=3)
    # solve()
