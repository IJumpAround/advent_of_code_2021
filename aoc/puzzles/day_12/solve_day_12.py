import copy
import os
from collections import defaultdict
from functools import reduce
from pathlib import Path
from pprint import pprint

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger

MAX_LITTLE_CAVE_VISTS = 1

def explore(cave, adj_list):
    print(adj_list)
    visited = defaultdict(int)
    print('Exploring cave')
    paths = []
    path = []
    _explore(cave, adj_list, visited, path, paths)
    print('\nleaving cave')
    pprint(paths)

    return paths

def is_small_cave(cave):
    if cave.lower() == cave:

        if cave not in ('start', 'end'):
            return True
    return False

def _explore(cave, adj_list, visited, path, paths):
    small_visited = []
    for k in visited:
        if k.lower() == k and k not in ('end', 'start'):
            small_visited.append(k)

    visited[cave] += 1
    path.append(cave)
    try:

        if is_small_cave(cave) and visited[cave] <= MAX_LITTLE_CAVE_VISTS:

            visited_twice_count = 0
            for sm in small_visited:
                if visited[sm] == 2:
                    visited_twice_count += 1

            if visited_twice_count == 2:
                path.pop()
                visited[cave] -= 1
                return
        elif is_small_cave(cave) and visited[cave] > MAX_LITTLE_CAVE_VISTS:
            path.pop()
            visited[cave] -= 1
            return
        elif cave == 'start' and len(visited) > 1:
            path.pop()
            visited[cave] -= 1
            return
        elif cave == 'end':
            paths.append(copy.deepcopy(path))
            visited[cave] -= 1
            path.pop()
            # print(',end')
            # print(path)
            # path.pop()
            return 1


        for adj in adj_list[cave]:
            if adj == cave or adj == path[-1] or adj == 'start':
                continue



            # nxt = copy.deepcopy(path)
            # nxt.append(adj)
            _explore(adj, adj_list, visited, path, paths)
            # visited[adj] -= 1
            # path.pop()
            # nxt.pop()
        path.pop()
        visited[cave] -= 1
    except RecursionError as e:
        print(path[-10:])
        print(cave)
        print(visited)
        print(e)
        exit()
        raise e

SE = ['start','end']

@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)


    vertices = []
    for line in list_input:
        vertices.append(line.split('-'))

    adj_list = []
    adj_list = defaultdict(list)
    reverse_adjacency = defaultdict(list)
    for v in vertices:
        s,e = v

        adj_list[s].append(e)
        if s not in adj_list[e]:

            adj_list[e].append(s)

        reverse_adjacency[e].append(s)

    # simplify graph
    remove = []
    print(adj_list)
    for n in adj_list:
        if n.lower() == n and n not in SE:
            if len(adj_list[n]) == 0:
                remove.append(n )

    for r in remove:
        others = reverse_adjacency[r]
        for other in others:
            adj_list[other].remove(r)
        print('removed one node')


    paths = explore('start', adj_list)
    answer = len(paths)
    print(f"The answer is {answer}\n")

    return answer

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    assert solve(_day_num, sample=False) == 4413

    MAX_LITTLE_CAVE_VISTS = 2
    assert solve(_day_num, sample=False) == 118803
