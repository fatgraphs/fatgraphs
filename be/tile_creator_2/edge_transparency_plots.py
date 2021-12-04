import math
import matplotlib.pyplot as plt
import os
import numpy as np

from be.tile_creator_2.edge_data import EdgeData
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.utils import calculate_diagonal_square_of_side


class EdgeTransparencyPlots:

    BIN_FREQUENCY = 50

    def __init__(self, graph_data: GraphData, gtm_args: GtmArgs, edge_data: EdgeData):
        self.sideGraphSpace = graph_data.get_graph_bound().get_side()
        self.zoomLevels = gtm_args.get_zoom_levels()
        self.edgeLengths = edge_data.get_lengths().values
        self.edgeTransparencies = edge_data.get_transparencies()
        self.minLength = int(min(self.edgeLengths))
        self.maxLength = int(max(self.edgeLengths))
        self.step = math.ceil((self.maxLength - self.minLength) / EdgeTransparencyPlots.BIN_FREQUENCY)
        self.tileSize = gtm_args.get_tile_size()

    def render(self, outputFolder):
        for zl in range(0, self.zoomLevels):
            self.generateDistributionImg(zl, outputFolder)

    def generateDistributionImg(self, zoomLevel, outputFolder):
        longestTheoreticalEdgePx = calculate_diagonal_square_of_side(self.tileSize)
        longestTheoreticalEdgeGraph = calculate_diagonal_square_of_side(self.sideGraphSpace)
        color = 'tab:red'
        fig, ax1 = plt.subplots()
        fig.suptitle("Zoom: " + str(zoomLevel), fontsize=15, x=0.1)

        def doLowerX():
            ax1.set_xlabel('Edge Len Graph Space ' +
                           "| Longest: " + str(round(self.maxLength, 2)) +
                           " | Square diagonal: " + str(round(longestTheoreticalEdgeGraph, 2)))
            hist = ax1.hist(self.edgeLengths.get(), bins=25, color=color, range=(0, longestTheoreticalEdgeGraph))
            ax1.set_xlim(0, longestTheoreticalEdgeGraph)
            return max(list(map(lambda a : a.get_height(), hist[2])))

        def doLeftY():
            y_title = "Count ( tot: " + str(len(self.edgeLengths)) + " )"
            ax1.set_ylabel(y_title, color=color)

        def doUpperX(height_highest_bar):
            xPixelDistance = ax1.twiny()
            xPixelDistance.set_xlabel("Edge Len Pixel")
            pixelLengthOfGraphSide = (self.tileSize * (2 ** zoomLevel))
            newTicks = list(map(lambda tick: int(tick * pixelLengthOfGraphSide / self.sideGraphSpace),
                                 ax1.get_xticks()))

            for i in range(0, (2 ** zoomLevel)):
                tile_mark = self.tileSize * (i + 1)
                xPixelDistance.axvline(x=tile_mark, ymin=0, ymax=self.maxLength, color='green')
                plt.text(tile_mark + 6, height_highest_bar / 12, str(i + 1), rotation=90, verticalalignment='top')

            xPixelDistance.set_xlim([0, longestTheoreticalEdgePx * (2 ** zoomLevel)])
            xPixelDistance.tick_params(axis='x', labelcolor=color)

        def doRightY():
            yyy = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            color = 'tab:blue'
            yyy.set_ylabel('Transparency', color=color)  # we already handled the x-label with ax1
            yyy.scatter(self.edgeLengths.get(), self.edgeTransparencies[zoomLevel].values, color=color)
            mean = np.mean(self.edgeTransparencies[zoomLevel])
            yyy.axvline(x=mean, ymin=0, ymax=max(self.edgeLengths.get()), color=color)
            yyy.tick_params(axis='y', labelcolor=color)

        heightHighestBar = doLowerX()
        doLeftY()
        doUpperX(heightHighestBar)
        doRightY()

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        name = "z_" + str(zoomLevel) + "_distribution" + ".png"
        join = os.path.join(outputFolder, name)
        plt.savefig(join)




