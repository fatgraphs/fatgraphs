import cugraph
import numpy as np
from cuml.neighbors.nearest_neighbors import NearestNeighbors
import cudf

from be.utils.utils import shift_and_scale, convert_graph_coordinate_to_map


class VisualLayout:

    default_force_atlas_2_options = {'max_iter': 500,
                                     'strong_gravity_mode': True,
                                     'barnes_hut_theta': 1.2,
                                     'outbound_attraction_distribution': False,
                                     'gravity': 1,
                                     'scaling_ratio': 1}

    def __init__(self, graph, config):
        self.graph = graph

        self.vertex_positions = self._run_force_atlas_2(graph.gpu_frame)

        temp_max = max(self.vertex_positions[0:-2]['x'].max(), self.vertex_positions[0:-2]['y'].max())
        temp_min = min(self.vertex_positions[0:-2]['x'].min(), self.vertex_positions[0:-2]['y'].min())

        # TODO
        # noverlap

        self._ensure_layout_is_square(temp_min, temp_max)
        self.edge_ids_to_positions = self.make_edge_ids_to_positions()
        self.edge_ids_to_positions_pixel = self.convert_to_pixel_space(config['tile_size'], temp_min, temp_max)
        self.edge_lengths = self._calculate_edge_lengths_graph_space()
        self.median_pixel_distance = self.compute_median_pixel_distance()
        self.vertex_sizes = self.calculate_vertices_size(graph.degrees['in_degree'], config['med_vertex_size'],
                                                         config['max_vertex_size'])
        log_amounts = np.log10(graph.edge_ids_to_amount['amount'].values + 1)  # amounts can be huge numbers, reduce the range
        self.edge_thickness = self.calculate_edges_thickness(log_amounts, config['med_edge_thickness'],
                                                             config['max_edge_thickness'])

        self.min = temp_min
        self.max = temp_max

        self.edge_transparencies = {}
        self.vertex_shapes = []

    def _run_force_atlas_2(self, gpu_graph):
        if not isinstance(gpu_graph, cugraph.structure.graph.Graph):
            raise TypeError("The cuGraph implementation of Force Atlas requires a gpu frame")
        # layout: x y vertex
        layout = cugraph.layout.force_atlas2(gpu_graph, **self.default_force_atlas_2_options)
        layout = layout.to_pandas()
        # layout = self._distribute_on_square_edges(layout)
        layout = layout.sort_values(['vertex'])
        layout = layout.reset_index(drop=True)
        return layout


    def compute_median_pixel_distance(self):
        vertices_once = self.edge_ids_to_positions_pixel.drop_duplicates(['source_x', 'source_y']).to_pandas()
        model = NearestNeighbors(n_neighbors=3)
        model.fit(vertices_once[['source_x_pixel', 'source_y_pixel']])
        distances, indices = model.kneighbors(vertices_once[['source_x_pixel', 'source_y_pixel']])
        median_pixel_distance = np.median(distances.flatten())
        return median_pixel_distance

    def _ensure_layout_is_square(self, min_coordinate, max_coordinate):
        self.vertex_positions.iloc[-1, 0:3] = [min_coordinate, min_coordinate, self.vertex_positions.iloc[-1, 0:3][2]]
        self.vertex_positions.iloc[-2, 0:3] = [max_coordinate, max_coordinate, self.vertex_positions.iloc[-2, 0:3][2]]

    def calculate_vertices_size(self, in_degrees, med_vertex_size, max_vertex_size):
        target_median = self.median_pixel_distance * med_vertex_size
        target_max = self.median_pixel_distance * max_vertex_size
        return shift_and_scale(in_degrees, target_median, target_max)

    def calculate_edges_thickness(self, amounts, med_edge_thickness, max_edge_thickness):
        target_median = self.median_pixel_distance * med_edge_thickness
        target_max = self.median_pixel_distance * max_edge_thickness
        return shift_and_scale(amounts, target_median, target_max)

    def _calculate_edge_lengths_graph_space(self):
        distances = ((self.edge_ids_to_positions['source_x'] - self.edge_ids_to_positions['target_x']) ** 2 + (
                self.edge_ids_to_positions['source_y'] - self.edge_ids_to_positions['target_y']) ** 2) ** 0.5
        return distances.to_array()

    def make_edge_ids_to_positions(self):
        vertex_x_y = cudf.from_pandas(self.vertex_positions)
        vertex_x_y = vertex_x_y.rename(columns={'x': 'source_x', 'y': 'source_y'})
        graph_positions = self.graph.edge_ids_to_amount_cudf.merge(vertex_x_y, left_on=['source_id'], right_on=['vertex'])
        vertex_x_y = vertex_x_y.rename(columns={'source_x': 'target_x', 'source_y': 'target_y'})
        graph_positions = graph_positions.merge(vertex_x_y, left_on=['target_id'], right_on=['vertex'])
        graph_positions = graph_positions.drop(columns=['vertex_x', 'vertex_y'])
        graph_positions = graph_positions.sort_values(by=['source_id', 'target_id']).reset_index(drop=True)
        return graph_positions

    def convert_to_pixel_space(self, tile_size, min_coordinate, max_coordinate):
        tile_coordinates = self.edge_ids_to_positions.apply_rows(convert_graph_coordinate_to_map,
                         incols=['source_x', 'source_y', 'target_x',
                                 'target_y'],
                         outcols=dict(source_x_pixel=np.float64, source_y_pixel=np.float64,
                                      target_x_pixel=np.float64, target_y_pixel=np.float64),
                         kwargs={'tile_size': tile_size,
                                 'min_coordinate': min_coordinate,
                                 'max_coordinate': max_coordinate})
        return tile_coordinates

    def _distribute_on_square_edges(self, layout):
        '''
        The layout generated by fa2 is a circle but the canvas is a rectangle.
        Therefore the corners of the rectangle won't have any node.
        We rectangularise the circular layout in order to better spread out the nodes.
        '''

        def scale(array, a, b):
            return (b - a) * ((array - min(array)) / max(1, (max(array) - min(array)))) + a

        # the layout is circular # to use more of the rectangular space, project onto a square
        u = layout["x"]
        v = layout["y"]
        umax = u.max()
        umin = u.min()
        vmax = v.max()
        vmin = v.min()

        # https://stats.stackexchange.com/a/178629

        u = scale(u, -0.9, 0.9)
        v = scale(v, -0.9, 0.9)

        # https://stackoverflow.com/a/32391780
        sqrt_two = np.sqrt(2)
        x = (0.5 * np.sqrt(2 + (u * u) - (v * v) + 2 * u * sqrt_two)) - (
                0.5 * np.sqrt(2 + (u * u) - (v * v) - 2 * u * sqrt_two))
        y = (0.5 * np.sqrt(2 - (u * u) + (v * v) + 2 * v * sqrt_two)) - (
                0.5 * np.sqrt(2 - (u * u) + (v * v) - 2 * v * sqrt_two))
        # for small graphs the above equation can produce nans
        x = np.nan_to_num(x)
        y = np.nan_to_num(y)
        x = scale(x, umin, umax)
        y = scale(y, vmin, vmax)
        layout["x"] = x
        layout["y"] = y
        return layout
