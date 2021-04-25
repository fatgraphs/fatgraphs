from be.configuration import MEDIUM_GRAPH_RAW_PATH, SMALL_GRAPH_RAW_PATH, CONFIGURATIONS, MOCK_LABELLED_RAW_PATH, \
    LABELS_PATH, METADATA_PATH, LARGE_GRAPH_RAW_PATH
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.render.renderer import GraphRenderer
import os
import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt

from be.tile_creator.src.token_graph_metadata import TokenGraphMetadata


def main(configurations):
    graph = TokenGraph(configurations['source'], {'dtype': {'amount': float}})
    visual_layout = VisualLayout(graph, configurations['tile_size'],
                                 configurations['med_vertex_size'], configurations['max_vertex_size'],
                                 configurations['med_edge_thickness'], configurations['max_edge_thickness'])

    metadata = TokenGraphMetadata(graph, visual_layout, configurations)
    gt_graph = GraphToolTokenGraph(graph, visual_layout, metadata, configurations)

    _generate_metadata_files(metadata, configurations)

    renderer = GraphRenderer(gt_graph, visual_layout, metadata, configurations)

    for zl in range(0, configurations['zoom_levels']):
        edge_lengths, scaled_values, x = compute_data_for_graph(gt_graph, renderer, zl)
        generate_distribution_img(edge_lengths, scaled_values, x, zl, configurations['output_folder'])

    renderer.render_tiles()


def compute_data_for_graph(gt_graph, renderer, zl):
    transparency_values = renderer.transparency_calculator.values
    edge_lengths = gt_graph.edge_length.a
    step = renderer.transparency_calculator.max_length // len(transparency_values[zl])
    x = list(
        range(int(renderer.transparency_calculator.min_length), int(renderer.transparency_calculator.max_length + 1),
              int(step)))
    scaled_values = np.asarray(transparency_values[zl])
    x = x[0:len(scaled_values)]
    return edge_lengths, scaled_values, x


def _generate_metadata_files(metadata, configuration_dictionary):
    output_folder = configuration_dictionary['output_folder']
    metadata.vertices_metadata.to_csv(
        os.path.join(output_folder,
                     CONFIGURATIONS['vertices_metadata_file_name']), index=False)
    metadata.graph_metadata.to_csv(
        os.path.join(output_folder,
                     CONFIGURATIONS['graph_metadata_file_name']), index=False)


def generate_distribution_img(edge_lengths, scaled_transparency_values, x, zoom_level, output_folder):
    # histo
    color = 'tab:red'
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Length Bins')
    y_title = "Count ( tot: " + str(len(edge_lengths)) + " )"
    ax1.set_ylabel(y_title, color=color)
    ax1.hist(edge_lengths, len(x), color=color)
    ax1.tick_params(axis='y')
    ax1.tick_params(axis='x')
    # ax1.xaxis.set_ticks(np.arange(min(x), max(x) + 1, 2.0))
    # ax1.yaxis.set_ticks(np.arange(min(x), max(x) + 1, 2.0))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Transparency', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, scaled_transparency_values, color=color)
    where = int(np.where(scaled_transparency_values == max(scaled_transparency_values))[0])
    ax2.axvline(x=x[where], ymin=0, ymax=max(edge_lengths))
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    name = "z_" + str(zoom_level) + "_distribution" + ".png"
    join = os.path.join(output_folder, name)
    plt.savefig(join)


if __name__ == '__main__':
    raise Exception("We are not supporting running main.py directly for tile generation, you should instead use " + \
                    "gtm.py as the entry point")
