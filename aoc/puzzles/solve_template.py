import os
from pathlib import Path

from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE

os.environ['LOG_LEVEL'] = 'INFO'
from aoc import logger
from aoc.utils import input_loader

L = logger
def solve(day, sample):
    L.info(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)



    L.info(f"The answer is {answer}\n")

    return answer

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=False)
    solve(_day_num, sample=True)
