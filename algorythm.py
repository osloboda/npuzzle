from queue import PriorityQueue
from copy import deepcopy
open_states = PriorityQueue()
closed_states = set()


def manhattan_dist(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)


"""def empty_bone_pos(bones):
    for i in bones:
        if 0 in i:
            return i.index(0), bones.index(i) 
"""
# Вес(F)
# каждой
# вершины
# вычисляется
# как
# сумма
# расстояния
# от
# начальной
# вершины
# до
# текущей(G)
# и
# эвристическое
# предположение
# о
# расстоянии
# от
# текущей
# вершины, до
# терминальной(H).Fi = Gi + Hi, где
# i - текущая
# вершина(состояние
# игрового
# поля).


def count_dist(x, y, bone):
    global end_state
    new_y, new_x = end_state.get_bone_coords(bone)
    return manhattan_dist(x, y, new_x, new_y)


def move(parent, x, y):
    new_bones = deepcopy(parent.bones)
    new_bones[parent.y][parent.x] = parent.bones[y][x]
    new_bones[y][x] = 0
    return new_bones


def new_state(x, y, parent):
    h = count_dist(x, y, parent.bones[y][x])
    if h > parent.h:
        return
    kid = State(parent, move(x, y, parent), h, x, y)
    open_states.put((h, kid))


def find_next_states(curr):
    global size
    x, y = curr.zero_coords
    if x < size:
        new_state(x + 1, y, curr)
    if x > 0:
        new_state(x - 1, y, curr)
    if y < size:
        new_state(x, y + 1, curr)
    if y > 0:
        new_state(x, y - 1, curr)


def main_cycle():
    while not open_states.empty():
        closed_states.add(hash(str(open_states.get().bones)))
        find_next_states(open_states.get())
        open_states.pop()

def run(start_bones):
    start = State(None, start_bones, 0, 0, 0)
    start.x, start.y = start.get_bone_coords(0)
    open_states.put(start.h, start)
    main_cycle()