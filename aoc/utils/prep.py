from typing import Optional

from aoc.puzzles import puzzles_path
from aoc.utils.input_loader import get_day_input_path, logger, day_int_to_str


def prompt_bool(prompt, choices: Optional[dict]=None) -> bool:
    choices = choices or {'y': True, 'n': False}

    prompt = f'{prompt} {list(choices.keys())}>'
    choice = ''
    while choice.lower() not in choices:
        choice = input(prompt)

    return choices[choice]

# def new_solver_template():
#
#     return (f"import os\n"
#
# os.environ['LOG_LEVEL'] = 'INFO'
# from aoc import logger"

def prepare_new_day(day: int):

    day = day_int_to_str(day)
    potential_input_path = get_day_input_path(day, raising=False)
    potential_puzzles_path = puzzles_path() / day

    if potential_input_path.is_dir():
        raise FileExistsError(potential_input_path)
    elif potential_puzzles_path.is_dir():
        raise FileExistsError(potential_puzzles_path)

    logger.info(f"Creating new day folders: \n{potential_puzzles_path}\n{potential_input_path}")
    if prompt_bool("Is this okay?"):
        potential_puzzles_path.mkdir()
        (potential_puzzles_path / '__init__.py').touch()
        (potential_puzzles_path / f'solve_{day}.py').touch()
        new_solver_file = potential_puzzles_path / f'solve_{day}'
        potential_input_path.mkdir()



if __name__ == '__main__':
    prepare_new_day(2)