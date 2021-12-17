import functools
import heapq
import os
from collections import defaultdict
from dataclasses import dataclass
from heapq import heapify
from pathlib import Path
from typing import Tuple

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger

INF = 9999999999999


@functools.cache
def sort_fn(node: 'Node'):
    return min(node.pos[0], node.pos[1]), max(node.pos[0], node.pos[1])


@dataclass()
class Node:
    pos: (int,int)
    risk: int
    visited: bool = False
    td: int = INF

    def __lt__(self, other):
        return self.td < other.td

    def __gt__(self, other):
        return not self.td > other.td

    def __eq__(self, other):
        return self.pos ==other.pos and self.td == other.td

    def __hash__(self):
        return hash((self.pos, self.risk))

    def __repr__(self):
        return f'<{self.pos} R[{self.risk}] TD[{self.td if self.td < INF else "∞"}]>'


class Edge:
    def __init__(self, n1: Node, n2:Node):
        self.l = n1
        self.r = n2

    @property
    def cost(self):
        return self.l.risk + self.r.risk

    @property
    def left(self) -> Tuple[int, int]:
        return self.l.pos

    @property
    def right(self) -> Tuple[int, int]:
        return self.r.pos

    def __repr__(self):
        return f'<{self.l}--{self.r} R={self.cost}>'


@functools.cache
def in_bounds(coord, H, W):

    if coord[0] >= H or coord[0] < 0 or coord[1] >= W or coord[1] < 0:
        return False
    return True


def increment_with_wrap(i: int, amount):
    i = int(i)
    s = i + amount
    if s > 9:
        s %= 9

    return s


@time_fn
def solve(day, sample, num_tiles):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")

    list_input = input_loader.load_file_as_list(day, sample)

    TILES = num_tiles
    risk_mtx = []
    adj_list = defaultdict(list)

    for v_tile in range(TILES):
        for row in list_input:
            mtx_row = []
            for r in range(TILES):
                new_values = []
                for i in row:

                    s = increment_with_wrap(i, r + v_tile)
                    new_values.append(s)
                mtx_row.extend(new_values)

            risk_mtx.append(mtx_row)

    H = len(risk_mtx)
    W = len(risk_mtx[0])

    Q = list()
    N = {}
    dest = Node((W-1, H-1), risk_mtx[-1][-1])
    start = Node((0, 0), 0, td=0)
    N[dest.pos] = dest
    N[start.pos] = start
    for i, row in enumerate(risk_mtx):
        for c, risk in enumerate(row):
            here = i,c

            u, d, r, l = (i - 1, c), (i + 1, c), (i, c + 1), (i, c - 1)

            n = N.get(here)
            if n is None:
                n = Node(here, risk)
                N[n.pos] = n
            Q.append(n)

            for adj in (u, d, r, l):
                if in_bounds(adj, H, W):
                    if adj in N:
                        other = N[adj]
                    else:
                        other = Node(adj, risk_mtx[adj[0]][adj[1]])
                        N[adj] = other

                    adj_list[n].append(other)
                    adj_list[other].append(n)

    count = 0
    prev = {}

    PQ = [start]
    heapify(PQ)
    while PQ:
        cur = heapq.heappop(PQ)
        cur.visited = True

        if cur.pos == dest.pos:
            print('found ending')
            break

        for n in adj_list[cur]:

            if not n.visited:

                td = n.risk + cur.td
                if n.td > td:
                    n.td = td
                    prev[n] = cur

                    heapq.heappush(PQ, n)

        count +=1

    nxt = dest
    path = [dest]
    while nxt in prev:
        c = prev[nxt]
        path.append(c)
        nxt = c

    print('path', list(reversed(path)))
    print('cost: ', sum([n.risk  for n in path]))

    # print_board(risk_mtx, path=path, show_cost=True)
    answer = dest.td
    print('answer', answer)

    return answer


def print_board(risk_mtx, U=None, path=None, show_cost=False):
    v_matx = []
    path_matrix = []
    for r in range(len(risk_mtx)):
        v_matx.append(['.' for _ in range(len(risk_mtx[r]))])
    for r in range(len(risk_mtx)):
        path_matrix.append(['.' for _ in range(len(risk_mtx[r]))])

    v_matx[0][0] = '+'
    if U:
        for u in U:
            f = u
            risk_mtx[f.pos[0]][f.pos[1]] = f.td if f.td < INF else 'x'
            v_matx[f.pos[0]][f.pos[1]] = '+' if f.visited else '.'

    if path:
        for p in path:
            path_matrix[p.pos[0]][p.pos[1]] = p.td

    n = 4 if show_cost else 1
    for i, r in enumerate(risk_mtx):
        seg = ''
        for j, c in enumerate(r):
            seg += f'{c:>3} '
        if path:
            seg += '\t'
            for j, c in enumerate(r):
                v = path_matrix[i][j]
                if not show_cost and v != '.':
                    v = '+'

                seg += f'{v:>{n}} '
        print(seg)


if __name__ == '__main__':
    # test123()
    _day_num = int(Path(__file__).stem.split('_')[-1])
    # solve(_day_num, sample=True)
    assert solve(_day_num, sample=False, num_tiles=1) == 386
    assert solve(_day_num, sample=False, num_tiles=5) == 2806
#