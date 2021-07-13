import math
import matplotlib.pyplot as plt
import os
import numpy as np
from be.utils.utils import calculateDiagonalSquareOfSide


class EdgeDistributionPlotRenderer:

    BIN_FREQUENCY = 50

    def __init__(self, configurations, visualLayout):
        self.sideGraphSpace = visualLayout.max - visualLayout.min
        self.zoomLevels = configurations['zoomLevels']
        self.edgeLengths = visualLayout.edgeLengths
        self.edgeTransparencies = visualLayout.edgeTransparencies
        self.outputFolder = configurations['outputFolder']
        self.minLength = int(min(self.edgeLengths))
        self.maxLength = int(max(self.edgeLengths))
        self.step = math.ceil((self.maxLength - self.minLength) / EdgeDistributionPlotRenderer.BIN_FREQUENCY)
        self.tileSize = configurations['tileSize']

    def render(self):
        for zl in range(0, self.zoomLevels):
            self.generateDistributionImg(list(self.edgeLengths), zl)

    def generateDistributionImg(self, edgeLengths, zoomLevel):
        longestTheoreticalEdgePx = calculateDiagonalSquareOfSide(self.tileSize)
        longestTheoreticalEdgeGraph = calculateDiagonalSquareOfSide(self.sideGraphSpace)
        color = 'tab:red'
        fig, ax1 = plt.subplots()
        fig.suptitle("Zoom: " + str(zoomLevel), fontsize=15, x=0.1)

        def doLowerX():
            ax1.set_xlabel('Edge Len Graph Space ' +
                           "| Longest: " + str(round(self.maxLength, 2)) +
                           " | Square diagonal: " + str(round(longestTheoreticalEdgeGraph, 2)))
            hist = ax1.hist(edgeLengths, bins=25, color=color, range=(0, longestTheoreticalEdgeGraph))
            ax1.set_xlim(0, longestTheoreticalEdgeGraph)
            # ax1.xaxis.set_minor_locator(MultipleLocator(5))
            return max(list(map(lambda a : a.get_height(), hist[2])))

        def doLeftY():
            y_title = "Count ( tot: " + str(len(edgeLengths)) + " )"
            ax1.set_ylabel(y_title, color=color)

        def doUpperX(height_highest_bar):
            xPixelDistance = ax1.twiny()
            xPixelDistance.set_xlabel("Edge Len Pixel")
            # x_pixel_distance.set_xlim(ax1.get_xlim())
            pixelLengthOfGraphSide = (self.tileSize * (2 ** zoomLevel))
            newTicks = list(map(lambda tick: int(tick * pixelLengthOfGraphSide / self.sideGraphSpace),
                                 ax1.get_xticks()))

            for i in range(0, (2 ** zoomLevel)):
                tile_mark = self.tileSize * (i + 1)
                xPixelDistance.axvline(x=tile_mark, ymin=0, ymax=self.maxLength, color='green')
                plt.text(tile_mark + 6, height_highest_bar / 12, str(i + 1), rotation=90, verticalalignment='top')

            xPixelDistance.set_xlim([0, longestTheoreticalEdgePx * (2 ** zoomLevel)])
            xPixelDistance.tick_params(axis='x', labelcolor=color)
            # x_pixel_distance.xaxis.set_minor_locator(MultipleLocator(10))

        def doRightY():
            yyy = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            color = 'tab:blue'
            yyy.set_ylabel('Transparency', color=color)  # we already handled the x-label with ax1
            yyy.scatter(self.edgeLengths, self.edgeTransparencies[zoomLevel], color=color)
            # where = int(np.where(y == max(y))[0][0])
            # yyy.axvline(x=x[where], ymin=0, ymax=max(edge_lengths))
            mean = np.mean(self.edgeTransparencies[zoomLevel])
            yyy.axvline(x=mean, ymin=0, ymax=max(edgeLengths), color=color)
            yyy.tick_params(axis='y', labelcolor=color)

        heightHighestBar = doLowerX()
        doLeftY()
        doUpperX(heightHighestBar)
        doRightY()

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        name = "z_" + str(zoomLevel) + "_distribution" + ".png"
        join = os.path.join(self.outputFolder, name)
        plt.savefig(join)




