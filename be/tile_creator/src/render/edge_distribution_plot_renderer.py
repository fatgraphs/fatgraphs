import math
import matplotlib.pyplot as plt
import os
import numpy as np
from be.utils.utils import calculate_diagonal_square_of_side


class EdgeDistributionPlotRenderer:

    BIN_FREQUENCY = 50

    def __init__(self, configurations, visual_layout):
        self.side_graph_space = visual_layout.max - visual_layout.min
        self.zoom_levels = configurations['zoom_levels']
        self.edge_lengths = visual_layout.edge_lengths
        self.edge_transparencies = visual_layout.edge_transparencies
        self.output_folder = configurations['output_folder']
        self.min_length = int(min(self.edge_lengths))
        self.max_length = int(max(self.edge_lengths))
        self.step = math.ceil((self.max_length - self.min_length) / EdgeDistributionPlotRenderer.BIN_FREQUENCY)
        self.tile_size = configurations['tile_size']

    def render(self):
        for zl in range(0, self.zoom_levels):
            self.generate_distribution_img(list(self.edge_lengths), zl)

    def generate_distribution_img(self, edge_lengths, zoom_level):
        longest_theoretical_edge_px = calculate_diagonal_square_of_side(self.tile_size)
        longest_theoretical_edge_graph = calculate_diagonal_square_of_side(self.side_graph_space)
        color = 'tab:red'
        fig, ax1 = plt.subplots()
        fig.suptitle("Zoom: " + str(zoom_level), fontsize=15, x=0.1)

        def do_lower_x():
            ax1.set_xlabel('Edge Len Graph Space ' +
                           "| Longest: " + str(round(self.max_length, 2)) +
                           " | Square diagonal: " + str(round(longest_theoretical_edge_graph, 2)))
            hist = ax1.hist(edge_lengths, bins=25, color=color, range=(0, longest_theoretical_edge_graph))
            ax1.set_xlim(0, longest_theoretical_edge_graph)
            # ax1.xaxis.set_minor_locator(MultipleLocator(5))
            return max(list(map(lambda a : a.get_height(), hist[2])))

        def do_left_y():
            y_title = "Count ( tot: " + str(len(edge_lengths)) + " )"
            ax1.set_ylabel(y_title, color=color)

        def do_upper_x(height_highest_bar):
            x_pixel_distance = ax1.twiny()
            x_pixel_distance.set_xlabel("Edge Len Pixel")
            # x_pixel_distance.set_xlim(ax1.get_xlim())
            pixel_length_of_graph_side = (self.tile_size * (2 ** zoom_level))
            new_ticks = list(map(lambda tick: int(tick * pixel_length_of_graph_side / self.side_graph_space),
                                 ax1.get_xticks()))

            for i in range(0, (2 ** zoom_level)):
                tile_mark = self.tile_size * (i + 1)
                x_pixel_distance.axvline(x=tile_mark, ymin=0, ymax=self.max_length, color='green')
                plt.text(tile_mark + 6, height_highest_bar / 12, str(i + 1), rotation=90, verticalalignment='top')

            x_pixel_distance.set_xlim([0, longest_theoretical_edge_px * (2 ** zoom_level)])
            x_pixel_distance.tick_params(axis='x', labelcolor=color)
            # x_pixel_distance.xaxis.set_minor_locator(MultipleLocator(10))

        def do_right_y():
            yyy = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            color = 'tab:blue'
            yyy.set_ylabel('Transparency', color=color)  # we already handled the x-label with ax1
            yyy.scatter(self.edge_lengths, self.edge_transparencies[zoom_level], color=color)
            # where = int(np.where(y == max(y))[0][0])
            # yyy.axvline(x=x[where], ymin=0, ymax=max(edge_lengths))
            mean = np.mean(self.edge_transparencies[zoom_level])
            yyy.axvline(x=mean, ymin=0, ymax=max(edge_lengths), color=color)
            yyy.tick_params(axis='y', labelcolor=color)

        height_highest_bar = do_lower_x()
        do_left_y()
        do_upper_x(height_highest_bar)
        do_right_y()

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        name = "z_" + str(zoom_level) + "_distribution" + ".png"
        join = os.path.join(self.output_folder, name)
        plt.savefig(join)




