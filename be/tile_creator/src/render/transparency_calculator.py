import cudf
import numpy as np

from be.utils import gauss


def set_transparency_gaussian(x, transparency, mean, std, min_out=0, max_out=1):
    for i, length in enumerate(x):
        transparency[i] = gauss(length, mean, std, min_out, max_out)


class TransparencyCalculator:

    def __init__(self, graph_side, configurations):
        """

        :param graph_side: graph space coordinates
        :param longest_edge: graph space coordinates
        :param configurations:
        """
        self.graph_side = graph_side
        self.tile_size = configurations['tile_size']
        self.zoom_levels = configurations['zoom_levels']
        self.std = configurations['std_transparency_as_percentage']
        self.min_t = configurations['min_transparency']
        self.max_t = configurations['max_transparency']

    def calculate_edge_transparencies(self, edge_lengths):
        transparencies = {}
        base_std = self.std * self.graph_side
        for zl in range(0, self.zoom_levels):
            # mean and std are the same for each zoom level
            mean_graph_space = min(self.graph_side,
                                   self.graph_side * (2 / (2 ** zl)))
            std_graph_space = base_std / max(1, zl * 1.5) # low std makes it spiky

            frame = cudf.DataFrame(edge_lengths, columns=['x'])
            trans = frame.apply_rows(set_transparency_gaussian,
                                     incols=['x'],
                                     outcols=dict(transparency=np.float64),
                                     kwargs={'mean': mean_graph_space,
                                             'std': std_graph_space,
                                             'min_out': self.min_t,
                                             'max_out': self.max_t})
            transparencies[zl] = trans.to_pandas()['transparency']

        return transparencies



