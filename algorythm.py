from queue import PriorityQueue
from npuzzle import State, n, end_state
from copy import deepcopy
open_states = PriorityQueue()


def manhattan_dist(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)


"""def empty_bone_pos(bones):
    for i in bones:
        if 0 in i:
            return i.index(0), bones.index(i) 
"""


def count_dist(x, y):
    global end_state
    manhattan_dist(x, y, end_state.x, end_state.y)


def move(parent, x, y):
    new_bones = deepcopy(parent.bones)
    new_bones[parent.y][parent.x] = parent.bones[y][x]
    new_bones[y][x] = 0
    return new_bones


def new_state(x, y, parent):
    theta = parent.g + 1 + count_dist(x, y)
    if theta > parent.theta:
        return
    kid = State(parent, move(x, y, parent), x, y, parent.g + 1, theta)
    open_states.put((theta, kid))

def find_next_states(curr):
    x, y = curr.zero_coords
    global n
    if x < n:
        new_state(x + 1, y, curr)
    if x > 0:
        new_state(x - 1, y, curr)
    if y < n:
        new_state(x, y + 1, curr)
    if y > 0:
        new_state(x, y - 1, curr)