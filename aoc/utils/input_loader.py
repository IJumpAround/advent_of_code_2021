import logging
from pathlib import Path

from aoc import aoc_root

logger = logging.getLogger(__name__)

def input_root() -> Path:
    return aoc_root().parent / 'puzzle_input'


def get_day_input_path(day: str):
    day_folder = input_root() / day
    try:
        assert day_folder.is_dir()
    except AssertionError as e:
        print(day_folder)
        raise e

    return day_folder


def load_file_as_string(day, filename='input.txt', chain_call=False) -> str:

    file = get_day_input_path(day) / filename


    logger.debug(f'Loading file: {file}')
    assert file.is_file()

    file_text = file.read_text()

    if not chain_call:
        logger.debug(file_text)

    return file_text


def load_file_as_newlines(day, filename='input.txt'):

    file = load_file_as_string(day, filename, chain_call=True)

    lines = file.splitlines()

    logger.debug(lines)
    return file.splitlines()



