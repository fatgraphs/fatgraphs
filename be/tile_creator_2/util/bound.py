class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bound:
    def __init__(self, minimum: Point, maximum: Point):
        self.min = minimum
        self.max = maximum

    def get_min_coord(self):
        return min(self.min.x, self.min.y)

    def get_max_coord(self):
        return max(self.max.x, self.max.y)

    def get_side(self):
        return self.get_max_coord() - self.get_min_coord()