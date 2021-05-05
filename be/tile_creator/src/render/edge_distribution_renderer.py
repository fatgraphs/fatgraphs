import cudf
import numpy as np
import matplotlib.pyplot as plt
import os

class EdgeDistributionRenderer:

    BIN_FREQUENCY = 50

    def __init__(self, zoom_levels, edge_lengths, transparency_calculator, output_folder, side_graph_space, tile_size):
        self.zoom_levels = zoom_levels
        self.edge_lenghts = edge_lengths
        self.output_folder = output_folder
        self.min_length = int(min(self.edge_lenghts))
        self.max_length = int(max(self.edge_lenghts))
        self.step = (self.max_length - self.min_length) // EdgeDistributionRenderer.BIN_FREQUENCY
        self.transparency_calculator = transparency_calculator
        self.transparency_x = list(range(self.min_length, self.max_length + 1, self.step))
        self.transparency_y = self.generate_y_transparency()
        self.side_graph_space = side_graph_space
        self.tile_size = tile_size

    def render(self):
        for zl in range(0, self.zoom_levels):
            self.generate_distribution_img(self.edge_lenghts, self.transparency_x, self.transparency_y[zl], zl)

    def generate_y_transparency(self):
        return self.transparency_calculator.calculate_edge_transparencies(self.transparency_x)

    def generate_distribution_img(self, edge_lengths, x, y, zoom_level):
        color = 'tab:red'
        fig, ax1 = plt.subplots()
        fig.suptitle("Zoom lvl: " + str(zoom_level) + " Longest Edge: " + str(self.max_length), fontsize=15)
        ax1.set_xlabel('Edge Len Graph')
        y_title = "Count ( tot: " + str(len(edge_lengths)) + " )"
        ax1.set_ylabel(y_title, color=color)
        ax1.hist(edge_lengths, len(x), color=color)
        ax1.set_xticks(ax1.get_xticks()[1::])
        ax1.tick_params(axis='y')
        ax1.tick_params(axis='x')
        for i in range(0, 2**zoom_level):
            ax1.axvline(x=self.side_graph_space / (2**zoom_level) * (i+1), ymin=0, ymax=self.max_length, color='orange')
            plt.text(self.side_graph_space / (2**zoom_level) * (i+1) + 6, self.max_length / 2, str(i + 1), rotation=90, verticalalignment='center')

        yyy = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        yyy.set_ylabel('Transparency', color=color)  # we already handled the x-label with ax1
        yyy.plot(x, y, color=color)
        where = int(np.where(y == max(y))[0])
        yyy.axvline(x=x[where], ymin=0, ymax=max(edge_lengths))
        yyy.tick_params(axis='y', labelcolor=color)


        x_pixel_distance = ax1.twiny()
        x_pixel_distance.set_xlabel("Edge Len Pixel")
        x_pixel_distance.set_xlim(ax1.get_xlim())
        new_ticks = list(map(lambda tick: int(tick * (self.tile_size * (2 ** zoom_level)) / self.side_graph_space),
                             ax1.get_xticks()))
        x_pixel_distance.set_xticks(ax1.get_xticks())
        x_pixel_distance.set_xticklabels(list(map(str, new_ticks)))
        x_pixel_distance.tick_params(axis='x', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        name = "z_" + str(zoom_level) + "_distribution" + ".png"
        join = os.path.join(self.output_folder, name)
        plt.savefig(join)
