from queue import PriorityQueue
from copy import deepcopy
from State import *
import numpy as np


def other_heuristics(bones1, bones2):
    i = 0
    for r1, r2 in zip(bones1, bones2):
        for c1, c2 in zip(r1, r2):
            if c1 != c2:
                i += 1
    return i


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Eval:
    def __init__(self, size, end_state, args):
        self.size = size
        self.end_state = end_state
        self.open_states = PriorityQueue()
        self.closed_states = set()
        self.tendstate = None
        self.args = args

        self.end_coords = [get_bone_coords(self.end_state.bones, i) for i in range(1, self.size ** 2)]

    def linear_conflict(self, bones1):
        i = 0

        for r1, r2 in zip(bones1, self.end_state.bones):
            for c1, c2 in zip(r1, r2):
                for _1, _2 in zip(r1, r2):
                    if c1 in r2 and _1 in r2:
                        if r2.index(c1) > r2.index(_1) and r1.index(c1) < r1.index(_1) or r2.index(c1) < r2.index(
                                _1) and r1.index(c1) > r1.index(_1):
                            i += 2
        tbones1 = np.array(bones1).T.tolist()
        for r1, r2 in zip(tbones1, self.tendstate):
            for c1, c2 in zip(r1, r2):
                for _1, _2 in zip(r1, r2):
                    if c1 in r2 and _1 in r2:
                        if r2.index(c1) > r2.index(_1) and r1.index(c1) < r1.index(_1) or r2.index(c1) < r2.index(
                                _1) and r1.index(c1) > r1.index(_1):
                            i += 2
        return i

    def count_distance(self, state, bone):
        y, x = et_bone_coords(state.bones, bone)
        new_y, new_x = get_bone_coords(self.end_state.bones, bone)
        return manhattan_dist(x, y, new_x, new_y)

    def count_dist(self, x, y, bone):
        new_y, new_x = get_bone_coords(self.end_state.bones, bone)
        return manhattan_dist(x, y, new_x, new_y)

    def total_dist(self, bones):
        sum = 0
        for y, row in enumerate(bones):
            for x, val in enumerate(row):
                if val:
                    end_y, end_x = self.end_coords[val - 1]
                    sum += manhattan_dist(x, y, end_x, end_y)
        return sum

    @staticmethod
    def move(parent, x, y):
        new_bones = deepcopy(parent.bones)
        new_bones[parent.y][parent.x] = parent.bones[y][x]
        new_bones[y][x] = 0
        return new_bones

    def new_state(self, x, y, parent, g):
        bones = self.move(parent, x, y)
        if hash(str(bones)) in self.closed_states:
            return
        if self.args.e == "linear":
            h = self.total_dist(bones) + self.linear_conflict(bones)
        elif self.args.e == "mini_e":
            h = other_heuristics(bones, self.end_state.bones)
        else:
            h = self.total_dist(bones)
        kid = State(parent, self.move(parent, x, y), g, h, x, y)
        self.open_states.put((kid.theta, id(kid), kid))

    def find_next_states(self, curr):
        x, y = curr.x, curr.y
        if x < self.size - 1:
            self.new_state(x + 1, y, curr, curr.g + 1)
        if x > 0:
            self.new_state(x - 1, y, curr, curr.g + 1)
        if y < self.size - 1:
            self.new_state(x, y + 1, curr, curr.g + 1)
        if y > 0:
            self.new_state(x, y - 1, curr, curr.g + 1)

    def main_cycle(self):
        i = 0
        while not self.open_states.empty():
            i += 1
            curr = self.open_states.get()[2]
            if curr.bones == self.end_state.bones:
                print("Finish state:\n")
                print('\n\n'.join(['\t'.join([str(cell) for cell in row]) for row in curr.bones]), '\n')
                break
            if self.args.s:
                print('\n\n'.join(['\t'.join([str(cell) for cell in row]) for row in curr.bones]), '\n', "------"*len(curr.bones))
            self.closed_states.add(hash(str(curr.bones)))
            self.find_next_states(curr)

        print("Iterations: ", i)

    def run(self, start_bones):
        self.tendstate = np.array(self.end_state.bones).T.tolist()
        start = State(None, start_bones, 0, 0, 0, 0)
        start.y, start.x = get_bone_coords(start.bones, 0)
        start.h = self.total_dist(start.bones)
        start.theta = start.h
        self.open_states.put((start.theta, id(start), start))
        self.main_cycle()
