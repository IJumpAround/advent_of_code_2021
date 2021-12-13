import os
import time
from collections import defaultdict
from pathlib import Path

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn
from aoc import logger
from aoc.utils import input_loader

L = logger

MAX_LITTLE_CAVE_VISTS = 1


def explore(cave, adj_list):
    visited = defaultdict(int)

    s = time.time()
    print('Exploring cave')
    paths = []
    path = []
    _explore(cave, adj_list, visited, path, paths)
    print(f'leaving cave after {time.time() - s} seconds exploring!')

    return paths


def is_small_cave(cave, permit_start_end=False):
    if cave.lower() != cave:
        return False

    if permit_start_end:
        return True
    elif not permit_start_end and cave not in ('start', 'end'):
        return True
    else:
        return False


def _explore(cave, adj_list, visited, path, paths):
    visited[cave] += 1
    path.append(cave)

    if is_small_cave(cave) and visited[cave]:

        if visited[cave] <= MAX_LITTLE_CAVE_VISTS:
            small_visited = []
            visited_twice_count = 0
            for k in visited:
                if is_small_cave(k):
                    small_visited.append(k)

                    if visited[k] == 2:
                        visited_twice_count += 1

                if visited_twice_count == 2:
                    path.pop()
                    visited[cave] -= 1
                    return
        else:
            path.pop()
            visited[cave] -= 1
            return
    elif cave == 'start' and len(visited) > 1:
        path.pop()
        visited[cave] -= 1
        return
    elif cave == 'end':
        paths.append([c for c in path])
        visited[cave] -= 1
        path.pop()
        return

    for adj in adj_list[cave]:
        if adj == path[-1]:
            continue

        _explore(adj, adj_list, visited, path, paths)

    path.pop()
    visited[cave] -= 1


SE = ['start', 'end']


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")

    list_input = input_loader.load_file_as_list(day, sample)

    vertices = []
    adj_list = defaultdict(list)
    for line in list_input:
        # vertices.append(line.split('-'))
        s, e = line.split('-')
        adj_list[s].append(e)
        if s not in adj_list[e]:
            adj_list[e].append(s)

    print(adj_list)

    paths = explore('start', adj_list)

    answer = len(paths)
    print(f"The answer is {answer}\n")

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    assert solve(_day_num, sample=False) == 4413  # ~.04

    MAX_LITTLE_CAVE_VISTS = 2
    assert solve(_day_num, sample=False) == 118803  # ~2.66

