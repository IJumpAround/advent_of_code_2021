import logging
from pathlib import Path

from aoc import aoc_root

logger = logging.getLogger(__name__)


def input_root() -> Path:
    return aoc_root().parent / 'puzzle_input'


def get_day_input_path(day: str, raising: bool = True):
    day_folder = input_root() / day
    try:
        assert day_folder.is_dir()
    except AssertionError as e:
        print(day_folder)
        if raising:
            raise e

    return day_folder


def _load_file_as_string(day: str, filename='input.txt') -> str:

    file = get_day_input_path(day) / filename

    logger.debug(f'Loading file: {file}')
    assert file.is_file()

    file_text = file.read_text()

    return file_text


def load_file_as_string(day: int, sample: bool = False):
    day = day_int_to_str(day)
    filename = get_filename(sample)

    text = _load_file_as_string(day, filename)
    logger.debug(text)

    return text


def load_file_as_list(day, sample=False):
    day = day_int_to_str(day)
    filename = get_filename(sample)

    file = _load_file_as_string(day, filename)

    lines = file.splitlines()

    logger.debug(lines)
    return file.splitlines()


def get_filename(sample=False):
    return 'input.txt' if not sample else 'sample.txt'


def day_int_to_str(day: int) -> str:

    return f'day_{day}'
