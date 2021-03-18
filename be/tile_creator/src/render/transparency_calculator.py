class TransparencyCalculator:

    def __init__(self, min_length, max_length, zoom_levels):
        self._do_args_check(max_length, min_length)
        self.min_length = min_length
        self.max_length = max_length
        self.zoom_levels = zoom_levels
        self.intervals = []
        self._calculate_intervals()

    def _do_args_check(self, max_length, min_length):
        if min_length < 0:
            raise Exception("min_length has to be positive")
        if max_length < min_length:
            raise Exception("You need to pass min_length first and max_length second")

    def _calculate_intervals(self):

        step = (self.max_length - self.min_length) / self.zoom_levels
        for i in range(0, self.zoom_levels):
            interval = (self.min_length + (i * step),
                        self.min_length + ((i + 1) * step))
            self.intervals.append(interval)
        self.intervals.reverse()

    def get_transparency(self, edge_length, zoom_level):
        # print("self.min_length: " + str(self.min_length))
        # print("self.max_length: " + str(self.max_length))

        interval = self.intervals[zoom_level]
        # print("interval: ", interval)
        length_equal_min = self.I(interval[0], self.min_length)
        result_left_equation = (edge_length - self.min_length + length_equal_min) / \
                               (interval[0] - self.min_length + length_equal_min)

        length_equal_max = self.I(interval[1], self.max_length)
        result_right_equation = (self.max_length - edge_length + length_equal_max) / \
                                (self.max_length - interval[1] + length_equal_max)

        return min(1, result_left_equation, result_right_equation)

    def I(self, a, b):
        return 1 if a == b else 0