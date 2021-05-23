import cudf
import numpy as np
import math
import matplotlib.pyplot as plt
import os

from matplotlib.ticker import MultipleLocator

from be.utils import calculate_diagonal_square_of_side


class EdgeDistributionPlotRenderer:
    BIN_FREQUENCY = 50

    def __init__(self, zoom_levels, edge_lengths, transparency_calculator, output_folder, side_graph_space, tile_size):
        self.side_graph_space = side_graph_space
        self.zoom_levels = zoom_levels
        self.edge_lenghts = edge_lengths
        self.output_folder = output_folder
        self.min_length = int(min(self.edge_lenghts))
        self.max_length = int(max(self.edge_lenghts))
        self.step = math.ceil((self.max_length - self.min_length) / EdgeDistributionPlotRenderer.BIN_FREQUENCY)
        self.transparency_calculator = transparency_calculator
        self.transparency_x = list(range(self.min_length, self.max_length + 1, self.step))
        self.transparency_y = self.generate_y_transparency()
        self.side_graph_space = side_graph_space
        self.tile_size = tile_size

    def render(self):
        for zl in range(0, self.zoom_levels):
            self.generate_distribution_img(list(self.edge_lenghts), self.transparency_x, self.transparency_y[zl], zl)

    def generate_y_transparency(self):
        return self.transparency_calculator.calculate_edge_transparencies(self.transparency_x)

    def generate_distribution_img(self, edge_lengths, x, y, zoom_level):
        # TODO refactor this mess
        longest_theoretical_edge_px = calculate_diagonal_square_of_side(self.tile_size)
        longest_theoretical_edge_graph = calculate_diagonal_square_of_side(self.side_graph_space)

        np.append(edge_lengths, longest_theoretical_edge_px)
        print(longest_theoretical_edge_px)
        print(longest_theoretical_edge_graph)

        color = 'tab:red'
        fig, ax1 = plt.subplots()
        fig.suptitle("Zoom: " + str(zoom_level), fontsize=15, x=0.1)
        ax1.set_xlabel('Edge Len Graph Space ' +
                       "| Longest: " + str(round(self.max_length, 2)) +
                       " | Square diagonal: " + str(round(longest_theoretical_edge_graph, 2)))
        y_title = "Count ( tot: " + str(len(edge_lengths)) + " )"
        ax1.set_ylabel(y_title, color=color)
        ax1.hist(edge_lengths, bins=len(x), color=color, range=(0, longest_theoretical_edge_graph))
        ax1.set_xlim(0, longest_theoretical_edge_graph)
        ax1.xaxis.set_minor_locator(MultipleLocator(5))
        # ax1.set_xticks(ax1.get_xticks()[1::])
        # ax1.tick_params(axis='y')
        # ax1.tick_params(axis='x')

        yyy = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        yyy.set_ylabel('Transparency', color=color)  # we already handled the x-label with ax1
        yyy.plot(x, y, color=color)
        where = int(np.where(y == max(y))[0][0])
        yyy.axvline(x=x[where], ymin=0, ymax=max(edge_lengths))
        yyy.tick_params(axis='y', labelcolor=color)

        x_pixel_distance = ax1.twiny()
        x_pixel_distance.set_xlabel("Edge Len Pixel")
        # x_pixel_distance.set_xlim(ax1.get_xlim())
        pixel_length_of_graph_side = (self.tile_size * (2 ** zoom_level))
        new_ticks = list(map(lambda tick: int(tick * pixel_length_of_graph_side / self.side_graph_space),
                             ax1.get_xticks()))

        longet_edge_contained_by_a_tile = longest_theoretical_edge_px * (2 ** zoom_level)
        for i in range(0, (2 ** zoom_level)):
            tile_mark = longest_theoretical_edge_px * (i +1)
            x_pixel_distance.axvline(x=tile_mark, ymin=0, ymax=self.max_length, color='green')
            plt.text(tile_mark + 6, self.max_length / 2, str(i + 1), rotation=90, verticalalignment='center')

        x_pixel_distance.set_xlim([0, longest_theoretical_edge_px * (2 ** zoom_level)])
        # x_pixel_distance.set_xticks(tile_mark)
        # x_pixel_distance.set_xticklabels(list(map(str, new_ticks)))
        x_pixel_distance.tick_params(axis='x', labelcolor=color)
        x_pixel_distance.xaxis.set_minor_locator(MultipleLocator(5))

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        name = "z_" + str(zoom_level) + "_distribution" + ".png"
        join = os.path.join(self.output_folder, name)
        plt.savefig(join)
