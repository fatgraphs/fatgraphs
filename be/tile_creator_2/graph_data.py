from cuml.neighbors.nearest_neighbors import NearestNeighbors

from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.util.bound import Point, Bound


class GraphData:

    def __init__(self):
        self.graph_space_bound : Bound = None
        self.pixel_space_bound : Bound = None
        self.median_pixel_distance = None
        self.vertex_count = None
        self.edge_count = None
        self.graph_name = None
        self.graph_category = None
        self.description = ''

    def to_json_camelcase(self):
        return dict(
            graphName=self.graph_name,
            graphCategory=self.graph_category,
            vertices=self.vertex_count,
            edges=self.edge_count,
            description=self.description,
        )


    def set_bounding_square(self, vertex_data):
        min_x_min_y = Point(
            vertex_data.cudf_frame['x'].min(),
            vertex_data.cudf_frame['y'].min()
        )
        max_x_max_y = Point(
            vertex_data.cudf_frame['x'].max(),
            vertex_data.cudf_frame['y'].max()
        )
        self.graph_space_bound = Bound(min_x_min_y, max_x_max_y)

    def set_bounding_square_pixel(self, gtm_args: GtmArgs):
        """
        The bounding box of the graph in pixel cooords depends only on the tile size defined in the configs
        :param gtm_args:
        :return:
        """
        self.pixel_space_bound = Bound(
            Point(0, 0),
            Point(gtm_args.get_tile_size(), gtm_args.get_tile_size()))

    def get_graph_bound(self):
        # the bound in graph space,
        # depend on the coordiantes returned by the algorithm used to compute vertex position (e.g. FA2)
        return self.graph_space_bound

    def set_median_pixel_distance(self, vertex_data):
        # todo document
        model = NearestNeighbors(n_neighbors=3)
        model.fit(vertex_data.cudf_frame[['x_pixel', 'y_pixel']])
        distances, indices = model.kneighbors(vertex_data.cudf_frame[['x_pixel', 'y_pixel']])
        self.median_pixel_distance = distances.mean(axis=1).median()

    def get_median_pixel_distance(self):
        return self.median_pixel_distance

    def set_edge_count(self, edge_data):
        self.edge_count = len(edge_data.cudf_frame)

    def set_vertex_count(self, vertex_data):
        self.vertex_count = len(vertex_data.cudf_frame)

    def set_graph_name(self, gtm_args: GtmArgs):
        self.graph_name = gtm_args.get_name()

    def set_graph_category(self, gtm_args: GtmArgs):
        self.graph_category = gtm_args.get_category()

    def get_pixel_bound(self):
        # the bounds in pixel, depends on the user-specified tile_size
        return self.pixel_space_bound

    def set_description(self, description):
        self.description = description
