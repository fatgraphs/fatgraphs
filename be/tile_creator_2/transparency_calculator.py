import math

import cudf
import numpy as np

from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.utils import gauss, calculate_diagonal_square_of_side, timeit


def setTransparencyGaussian(x, transparency, mean, std, min_out=0, max_out=1):
    for i, length in enumerate(x):
        transparency[i] = gauss(length, mean, std, min_out, max_out)


class TransparencyCalculator:

    def __init__(self, graph_data: GraphData, gtm_args: GtmArgs):
        """

        :param graph_side: graph space coordinates
        :param longest_edge: graph space coordinates
        :param configurations:
        """
        self.side_graph_space = graph_data.graph_space_bound.get_side()
        self.gtm_args = gtm_args
        # self.tileSize = configurations['tile_size']
        # self.zoomLevels = configurations['zoom_levels']
        # self.std = configurations['std_transparency_as_percentage']
        # self.tileBasedMean = configurations["tile_based_mean_transparency"]
        # self.minT = configurations['min_transparency']
        # self.maxT = configurations['max_transparency']

    @timeit("Calculating edge transparencies")
    def calculateEdgeTransparencies(self, edgeLengths):
        longestTheoreticalEdge = calculate_diagonal_square_of_side(self.side_graph_space)
        if math.floor(max(edgeLengths)) > longestTheoreticalEdge:
            raise Exception(
                "You are trying to estimate the transparency of an edge that is longer than the diagonal of the \n"
                "square into which the graph is enclosed, the side of the square is {0} but there is an edge that is \n"
                "{1} , the max length is {2}".format(self.side_graph_space, max(edgeLengths), longestTheoreticalEdge))

        transparencies = {}
        for zl in range(0, self.gtm_args.get_zoom_levels()):
            meanGraphSpace = self.side_graph_space * (self.gtm_args.get_tile_based_mean_transparency() / (2 ** zl))
            stdGraphSpace = self.side_graph_space * (self.gtm_args.get_std_percentage() / (2 ** zl))

            frame = cudf.DataFrame(edgeLengths, columns=['x'])
            trans = frame.apply_rows(setTransparencyGaussian,
                                    incols=['x'],
                                    outcols=dict(transparency=np.float64),
                                    kwargs={'mean': meanGraphSpace,
                                            'std': stdGraphSpace,
                                            'min_out': self.gtm_args.get_min_transparency(),
                                            'max_out': self.gtm_args.get_max_transparency()})
            transparencies[zl] = trans.to_pandas()['transparency']

        return transparencies
