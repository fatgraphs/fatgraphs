import math

import cudf
import numpy as np

from be.utils.utils import gauss, calculateDiagonalSquareOfSide


def setTransparencyGaussian(x, transparency, mean, std, min_out=0, max_out=1):
    for i, length in enumerate(x):
        transparency[i] = gauss(length, mean, std, min_out, max_out)


class TransparencyCalculator:

    def __init__(self, graphSide, configurations):
        """

        :param graph_side: graph space coordinates
        :param longest_edge: graph space coordinates
        :param configurations:
        """
        self.graphSide = graphSide
        self.tileSize = configurations['tile_size']
        self.zoomLevels = configurations['zoom_levels']
        self.std = configurations['std_transparency_as_percentage']
        self.tileBasedMean = configurations["tile_based_mean_transparency"]
        self.minT = configurations['min_transparency']
        self.maxT = configurations['max_transparency']

    def calculateEdgeTransparencies(self, edgeLengths):
        longestTheoreticalEdge = calculateDiagonalSquareOfSide(self.graphSide)
        if math.floor(max(edgeLengths)) > longestTheoreticalEdge:
            raise Exception(
                "You are trying to estimate the transparency of an edge that is longer than the diagonal of the \n"
                "square into which the graph is enclosed, the side of the square is {0} but there is an edge that is \n"
                "{1} , the max length is {2}".format(self.graphSide, max(edgeLengths), longestTheoreticalEdge))

        transparencies = {}
        for zl in range(0, self.zoomLevels):
            meanGraphSpace = self.graphSide * (self.tileBasedMean / (2 ** zl))
            stdGraphSpace = self.graphSide * (self.std / (2 ** zl))

            frame = cudf.DataFrame(edgeLengths, columns=['x'])
            trans = frame.apply_rows(setTransparencyGaussian,
                                    incols=['x'],
                                    outcols=dict(transparency=np.float64),
                                    kwargs={'mean': meanGraphSpace,
                                            'std': stdGraphSpace,
                                            'min_out': self.minT,
                                            'max_out': self.maxT})
            transparencies[zl] = trans.to_pandas()['transparency']

        return transparencies
