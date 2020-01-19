import os
import sys


def move(x, y, state):
    for row in state:
        for col in row:
            if col == 0:
                prev = state[y][x]
                state[y][x] = col
                col = prev

class State:
    def __init__(self, both, kids):
        self.both = both
        self.kids = self.val = kids


if __name__ == "__main__":
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print("Usage: python3 npuzzle.py map.txt")
        exit()
    data = []
    with open(sys.argv[1]) as f:
        for line in f:
            subdata = []
            for x in line.split():
                if str(x).isdigit():
                    subdata.append(int(x))
            if (subdata):
                data.append(subdata)
    size = data[0][0]
    data.remove(data[0])
    print(size, '\n', data)
