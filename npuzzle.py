import os
import sys
import argparse


class State:
    def __init__(self, both, kids, bones):
        self.both = both
        self.kids = kids
        self.bones = bones
        self.theta = 0



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get arguments')
    parser.add_argument('-f', action='store', dest='f', help='Input file name')
    args = parser.parse_args()

    if not args.f or not os.path.exists(args.f):
        print("usage: npuzzle.py [-h] [-f] \n positional arguments:  -f     Input file name \n\noptional arguments: -h for help")
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
