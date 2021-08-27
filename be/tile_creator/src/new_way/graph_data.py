from cuml.neighbors.nearest_neighbors import NearestNeighbors
from pandas import DataFrame

from be.tile_creator.src.new_way.gtm_args import GtmArgs


class GraphData:
    class Bound:
        def __init__(self, minimum, maximum):
            self.min = minimum
            self.max = maximum

    def __init__(self):
        self.vertex_bounding_square = None
        self.vertex_bounding_square_pixel = None
        self.median_pixel_distance = None

    def set_bounding_square(self, positions: DataFrame):
        vmin = min(positions[0:-2]['x'].min(), positions[0:-2]['y'].min())
        vmax = max(positions[0:-2]['x'].max(), positions[0:-2]['y'].max())
        self.vertex_bounding_square = GraphData.Bound(vmin, vmax)

    def set_bounding_square_pixel(self, gtm_args: GtmArgs):
        self.vertex_bounding_square_pixel = GraphData.Bound(0, gtm_args.get_tile_size())

    def get_vertex_bound(self, pixel=False):
        if pixel:
            return self.vertex_bounding_square_pixel
        return self.vertex_bounding_square

    def set_median_pixel_distance(self, vertex_positions_pixel):
        model = NearestNeighbors(n_neighbors=3)
        model.fit(vertex_positions_pixel[['x_pixel', 'y_pixel']])
        distances, indices = model.kneighbors(vertex_positions_pixel[['x_pixel', 'y_pixel']])
        self.median_pixel_distance = distances.mean(axis=1).median()

    def get_median_pixel_distance(self):
        return self.median_pixel_distance
