import numpy as np

class TransparencyCalculator:

    def __init__(self, min_length, max_length, zoom_levels):
        self._do_args_check(max_length, min_length, zoom_levels)
        self.min_length = min_length
        self.max_length = max_length
        self.zoom_levels = zoom_levels
        self.intervals = []
        self._calculate_intervals()
        self.max_std = 30 / 3

    def _do_args_check(self, max_length, min_length, zoom_levels):
        if min_length < 0:
            raise Exception("min_length has to be positive")
        if max_length < min_length:
            raise Exception("You need to pass min_length first and max_length second")
        if zoom_levels < 2:
            raise Exception("The minimum zoom level should be 2")

    def _calculate_intervals(self):

        step = (self.max_length - self.min_length) / self.zoom_levels
        for i in range(0, self.zoom_levels):
            interval = (self.min_length + (i * step),
                        self.min_length + ((i + 1) * step))
            self.intervals.append(interval)
        self.intervals.reverse()

    def get_transparency(self, edge_length, zoom_level):
        if not zoom_level < self.zoom_levels and zoom_level > 0:
            raise Exception("zoom level needs to be between 0 and the max zoom leve ({0})".format(self.zoom_levels))

        return self.gaussian_bumps(edge_length, zoom_level)

    def gaussian_bumps(self, edge_length, zoom_level):
        '''
        A strategy to calculate transparency.
        '''
        std = self.max_std * (2 / self.zoom_levels)
        if zoom_level == 0:
            return self.gauss(edge_length, self.max_length, std)
        if zoom_level == self.zoom_levels - 1:
            return self.gauss(edge_length, self.min_length, std)

        zooms_left_plus_one = self.zoom_levels - 2 + 1
        step = (self.max_length - self.min_length) / (zooms_left_plus_one)
        return self.gauss(edge_length, step * (zooms_left_plus_one - zoom_level), std)


    def platou_and_linear_decrease(self, edge_length, zoom_level):
        '''
        A strategy to calculate transparency.
        Given the zoom level, all edges withing a certain length range have
        transparency = 1 (fully opaque). Edges with a length that is outside such range have linearly decreasing transparency.
        '''
        interval = self.intervals[zoom_level]
        # print("interval: ", interval)
        length_equal_min = self.I(interval[0], self.min_length)
        result_left_equation = (edge_length - self.min_length + length_equal_min) / \
                               (interval[0] - self.min_length + length_equal_min)
        length_equal_max = self.I(interval[1], self.max_length)
        result_right_equation = (self.max_length - edge_length + length_equal_max) / \
                                (self.max_length - interval[1] + length_equal_max)
        return min(1, result_left_equation, result_right_equation)

    def _I(self, a, b):
        '''
        Identity function
        '''
        return 1 if a == b else 0

    def _gauss(self, x, mu, sig):
        '''
        Compute gaussian function
        '''
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

