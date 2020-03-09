import os
import argparse
from algorythm import *
from State import *


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
    for row in m:
        if n * n in row:
            row[row.index(n*n)] = 0

    return m


def to_1d_matrix(matrix, n):
    matrix_1d = []
    dx, dy = [0, 1, 0, -1], [1, 0, -1, 0]
    x, y = 0, -1
    for i in range(n + n - 1):
        for _ in range((n + n - i) // 2):
            x += dx[i % 4]
            y += dy[i % 4]
            matrix_1d.append(matrix[x][y])
    return matrix_1d


def is_solvable(matrix, n):
    inv = 0
    for i in range(n * n):
        if matrix[i]:
            for j in range(i):
                if matrix[j] > matrix[i]:
                    inv += 1
                j += 1
    inv += 1 + matrix.index(0) // 4
    if inv % 2:
        return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get arguments')
    parser.add_argument('-f', action='store', dest='f', help='Input file name')
    parser.add_argument('-e', action='store', dest='e', help='Heuristic (linear, manhattan, mini_e)')
    parser.add_argument('-s', action='store_true', default=False, help='Show statistic')
    args = parser.parse_args()

    if not args.f or not os.path.exists(args.f):
        print("usage: npuzzle.py [-h, -s] [-f, -e] \npositional arguments:  -f     Input file name\n"
              "                       -e     Heuristic name (linear, manhattan, mini_e)"
              " \n\noptional arguments:    -h     Help\n                       -s     Show statistic")
        exit()
    data = []
    with open(args.f) as f:
        for line in f:
            if '#' in line:
                end = line.index('#')
                line = line[0:end]
            subdata = []
            for x in line.split():
                if x.isdigit():
                    subdata.append(int(x))
                else:
                    print("Invalid map!")
                    exit()
            if (subdata):
                data.append(subdata)
    size = data[0][0]
    data.remove(data[0])
    end = spiral_matrix(size)
    copy = np.array(data).flatten().tolist()
    for i in range(size * size):
        try:
            copy.remove(i)
        except:
            pass
    if copy:
        print("Invalid map!")
        exit()
    if not is_solvable(to_1d_matrix(data, size), size):
        print("Unsolvabe map!")
        exit()
    eval = Eval(size, State(None, end, 0, 0, 0, 0,), args)
    print('Start state:\n')
    print('\n\n'.join(['\t'.join([str(cell) for cell in row]) for row in data]), '\n')
    eval.run(data)
