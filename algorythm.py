from queue import PriorityQueue
from copy import deepcopy
from State import *


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Eval:
    def __init__(self, size, end_state):
        self.size = size
        self.end_state = end_state
        self.open_states = PriorityQueue()
        self.closed_states = set()
        self.end_coords = [get_bone_coords(self.end_state.bones, i) for i in range(1, self.size ** 2)]

    def count_distance(self, state, bone):
        y, x = get_bone_coords(state.bones, bone)
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

    def new_state(self, x, y, parent, g, parent_h):
        bones = self.move(parent, x, y)
        if hash(str(bones)) in self.closed_states:
            return
        h = self.total_dist(bones)
        kid = State(parent, self.move(parent, x, y), g, h, x, y)
        self.open_states.put((kid.theta, id(kid), kid))

    def find_next_states(self, curr):
        x, y = curr.x, curr.y
        curr_bone_h = self.count_dist(x, y, curr.bones[y][x])
        if x < self.size - 1:
            self.new_state(x + 1, y, curr, curr.g + 1, curr_bone_h)
        if x > 0:
            self.new_state(x - 1, y, curr, curr.g + 1, curr_bone_h)
        if y < self.size - 1:
            self.new_state(x, y + 1, curr, curr.g + 1, curr_bone_h)
        if y > 0:
            self.new_state(x, y - 1, curr, curr.g + 1, curr_bone_h)

    def main_cycle(self):
        i = 0
        while not self.open_states.empty():
            i += 1
            curr = self.open_states.get()[2]
            if curr.bones == self.end_state.bones:
                print(curr.bones)
                break
            self.closed_states.add(hash(str(curr.bones)))
            self.find_next_states(curr)
        print(i)

    def run(self, start_bones):
        start = State(None, start_bones, 0, 0, 0, 0)
        start.x, start.y = get_bone_coords(start.bones, 0)
        start.h = self.total_dist(start.bones)
        start.theta = start.h
        print(start.h)
        self.open_states.put((start.theta, id(start), start))
        self.main_cycle()
