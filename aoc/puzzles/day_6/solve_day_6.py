import os
from functools import reduce
from pathlib import Path

os.environ['LOG_LEVEL'] = 'DEBUG'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


class Fish:

    def __init__(self, age, just_spawned=False):
        self.age = age
        self.just_spawned = just_spawned
        self.birth_count = 0
        self.count = 1

    def tick(self):
        # if self.just_spawned:
        #     self.just_spawned = False
        #     return

        if self.age == 0:
            self.age = 6
            self.birth_count += 1
            return True

        self.age -= 1

    def __eq__(self, other):
        return self.age == other

    def __str__(self):
        return str(self.age)

    def __repr__(self):
        return f'{self.age}'


class School(Fish):

    def __init__(self, age, count):
        super(School, self).__init__(age)
        self.count = count

    def __eq__(self, other):
        return self.age == other

    def __getitem__(self, item):
        return self.age == item

    def __str__(self):
        return f'{self.age}x{self.count}'

    def __repr__(self):
        return f'{self.age}x{self.count}'

def next_day(schools):
    new_fishies = []
    for school in schools:
        new_fish = school.tick()

        if new_fish:
            # if 8 in fishies:

            new_fishies.append(School(8, count=school.count))

    return new_fishies


def update_schools(schools, just_spawned_school):
    # new_school = {v.age: v, for v in schools.values()}
    updated_schools = dict()
    for k in schools.keys():
        s = schools[k]

        if s.age in updated_schools:
            updated_schools[s.age].count += s.count
        else:
            updated_schools[s.age] = s

    for f in just_spawned_school:
        if f.age in updated_schools:
            updated_schools[f.age].count += f.count
        else:
            updated_schools[f.age] = f

    return updated_schools

@time_fn
def solve(day, sample, days):
    L.info(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    fish = [School(int(fish), 1) for fish in string_input.split(',')]

    L.info(fish)
    schools = {}
    schools = update_schools(schools, fish)

    L.info(schools)


    # growth rate 1 per 7 days
    # fish = num days to spawn
    # childhood -> 1st cycle = 2 days
    # on birth reset to 6 not 7
    # new fish starts with 8 count down next day




    for i in range(days):
        new_fish = next_day(schools.values())
        schools = update_schools(schools, new_fish)
        # fish += new_fish
        L.info(f'Day: {i + 1}')
        L.debug(f'After {i+1} Days {schools}')
    L.info(schools)
    answer1 = len(fish)
    answer = sum(map(lambda s: s.count, schools.values()))

    L.info(f"The answer is {answer}\n")
    return answer

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    assert solve(_day_num, sample=True, days=80) == 5934
    assert solve(_day_num, sample=False, days=80) == 386536
    assert solve(_day_num, sample=True, days=256) == 26984457539
    assert solve(_day_num, sample=False, days=256) == 1732821262171

