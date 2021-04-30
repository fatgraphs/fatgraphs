import numpy as np
import matplotlib.pyplot as plt
import os


class EdgeDistributionRenderer:
    def __init__(self, zoom_levels, edge_lengths, transparency_calculator, output_folder, side_graph_space, tile_size):
        self.zoom_levels = zoom_levels
        self.edge_lenghts = edge_lengths
        self.output_folder = output_folder
        self.transparency_calculator = transparency_calculator
        self.min_length = int(min(self.edge_lenghts))
        self.max_length = int(max(self.edge_lenghts))
        self.zoom_to_transparencies = self.generate_transparency_values_for_plots()
        self.side_graph_space = side_graph_space
        self.tile_size = tile_size

    def render(self):
        for zl in range(0, self.zoom_levels):
            x, y = self.compute_x_and_y_for_plot(zl)
            self.generate_distribution_img(self.edge_lenghts, x, y, zl)

    def generate_transparency_values_for_plots(self):
        zoom_to_transparencies = {}
        for zoom_level in range(0, self.zoom_levels
                                ):
            zoom_to_transparencies[zoom_level] = []
            for edge_length in range(self.min_length, self.max_length + 1, 20):
                zoom_to_transparencies[zoom_level].append(
                    self.transparency_calculator.get_transparency(edge_length, zoom_level))
        return zoom_to_transparencies

    def compute_x_and_y_for_plot(self, zl):
        step = self.max_length // len(self.zoom_to_transparencies[zl])
        x_edge_length = list(
            range(self.min_length,
                  self.max_length,
                  int(step)))
        y_transparency = np.asarray(self.zoom_to_transparencies[zl])
        x_edge_length = x_edge_length[0:len(y_transparency)]
        return x_edge_length, y_transparency

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

        y_transparency = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        y_transparency.set_ylabel('Transparency', color=color)  # we already handled the x-label with ax1
        y_transparency.plot(x, y, color=color)
        where = int(np.where(y == max(y))[0])
        y_transparency.axvline(x=x[where], ymin=0, ymax=max(edge_lengths))
        y_transparency.tick_params(axis='y', labelcolor=color)


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
