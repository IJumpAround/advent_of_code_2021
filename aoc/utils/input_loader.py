import logging

from aoc.utils.consts import get_filename, day_int_to_str, input_root, INPUT_FILE

logger = logging.getLogger(__name__)


def get_day_input_path(day: str, raising: bool = True):
    day_folder = input_root() / day
    try:
        assert day_folder.is_dir()
    except AssertionError as e:
        logger.error(day_folder)
        if raising:
            raise e

    return day_folder


def _load_file_as_string(day: str, filename=INPUT_FILE) -> str:

    file = get_day_input_path(day) / filename

    logger.debug(f'Loading file: {file}')
    assert file.is_file()

    file_text = file.read_text()

    return file_text


def load_file_as_string(day: int, sample: bool = False):
    day = day_int_to_str(day)
    filename = get_filename(sample)

    text = _load_file_as_string(day, filename)
    logger.debug(f'File string content\n{text}\n')

    return text


def load_file_as_list(day, sample=False):
    day = day_int_to_str(day)
    filename = get_filename(sample)

    file = _load_file_as_string(day, filename)

    lines = file.splitlines()

    logger.debug(f"File list content: \n{lines}\n")
    return file.splitlines()
