class State:
    def __init__(self, parent, bones, g, h, x, y):
        self.parent = parent
        self.bones = bones
        self.g = g
        self.h = h
        self.x = x
        self.y = y
        self.theta = g + h


def get_bone_coords(bones, bone):
    for y in bones:
        for x in y:
            if x == bone:
                return bones.index(y), y.index(x)
