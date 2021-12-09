import os
from functools import reduce
from pathlib import Path

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


def map_basin(heightmap, location, explored):
    print('\nMapping this basin starting at', location, heightmap[location[0]][location[1]])

    print()
    size = _map_basin(heightmap, location, explored)
    print(" Explored basin of size ", size)

    return size

def _map_basin(heightmap, location, explored):
    H = len(heightmap)
    W = len(heightmap[0])
    if location[0] < 0 or location[1] < 0 or location[1] == W or location[0] == H:
        return 0

    cell = heightmap[location[0]][location[1]]

    if location in explored or cell == 9:
        return 0
    else:
        print(cell,location, end=',')

    count = 1
    explored.add(location)
    x, y = location
    steps = [(x, y + 1),
             (x, y - 1),
             (x - 1, y),
             (x + 1, y)]

    for step in steps:
        count += _map_basin(heightmap, step, explored)

    return count

@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    heightmap = []
    for row in list_input:
        new_row = [int(ch) for ch in row]
        heightmap.append(new_row)
    # print(heightmap)

    lowest = []
    H = len(heightmap)
    W = len(heightmap[0])
    print(H, W)
    basins = []
    for x, row in enumerate(heightmap[:len(heightmap)]):
        for y, cell in enumerate(row[:len(row)]):

            # print(x, y)
            d = heightmap[x][y + 1] if y < W - 1 else 999
            u = heightmap[x][y - 1] if y > 0 else 999
            l = heightmap[x - 1][y] if x >= 0 else 999
            r = heightmap[x + 1][y] if x < H - 1 else 999

            low = min(d, u, l, r, cell)

            # print(d, u, l, r, cell)
            # print(low)
            adj = [d, u, l, r]
            if low == cell and low not in adj:
                print(adj, cell)
                lowest.append(cell)
                basins.append(map_basin(heightmap, (x,y), set()))


    risk = 0
    for num in lowest:
        risk += num + 1
    answer = risk

    print(sorted(basins, reverse=True))
    basin_answer = reduce(lambda x,y: x* y, sorted(basins, reverse=True)[:3])
    print(f"The answer is {answer}\n")
    print('basins ',basins)
    print('largest basins x ', basin_answer)
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
