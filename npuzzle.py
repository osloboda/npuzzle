import os
import argparse


def spiral_matrix(n):
    m = [[0] * n for _ in range(n)]
    dx, dy = [0, 1, 0, -1], [1, 0, -1, 0]
    x, y, c = 0, -1, 1
    for i in range(n + n - 1):
        for j in range((n + n - i) // 2):
            x += dx[i % 4]
            y += dy[i % 4]
            m[x][y] = c
            c += 1
    m[n * n == n * n][n * n == n * n] = 0
    return m


class State:
    def __init__(self, parent, bones, x, y, g, theta):
        self.parent = parent
        self.bones = bones
        self.g = 0
        self.theta = 0
        self.x = x
        self.y = y


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get arguments')
    parser.add_argument('-f', action='store', dest='f', help='Input file name')
    args = parser.parse_args()

    if not args.f or not os.path.exists(args.f):
        print("usage: npuzzle.py [-h] [-f] \n positional arguments:  -f     Input file name"
              " \n\noptional arguments: -h for help")
        exit()
    data = []
    with open(args.f) as f:
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

    end_state = State(None, spiral_matrix(size), 0, 0, 0, 0)

    print(end_state.bones)
