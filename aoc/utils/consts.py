from pathlib import Path

from aoc import aoc_root, puzzles


INPUT_FILE = 'input.txt'
SAMPLE_FILE = 'sample.txt'


def get_filename(sample=False):
    return INPUT_FILE if not sample else SAMPLE_FILE


def day_int_to_str(day: int) -> str:

    return f'day_{day}'


def input_root() -> Path:
    return aoc_root().parent / 'puzzle_input'


def template_solve_file() -> Path:
    return (Path(puzzles.__file__).parent / 'solve_template.py').absolute()
