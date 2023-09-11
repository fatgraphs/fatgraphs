from be.tile_creator_2.edge_data import EdgeData #noqa
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.transparency_calculator import TransparencyCalculator

from .fixtures_edge import *  # noqa
from .fixtures_graph import *  # noqa
from .fixtures_vertex import *  # noqa
from .fixtures import *  # noqa


class TestEdgeData:

    def test_init(self, graph_data_median: GraphData, gtm_args: GtmArgs):
        tc = TransparencyCalculator(graph_data_median, gtm_args)
        assert tc.gtm_args is not None
        assert tc.side_graph_space > 0, "The length of the bounding square of the graph was null"

    def test_calculate(self, graph_data_median: GraphData, edge_data_lengths: EdgeData, gtm_args: GtmArgs):
        tc = TransparencyCalculator(graph_data_median, gtm_args)
        transparencies = tc.calculateEdgeTransparencies(edge_data_lengths.get_lengths().to_numpy())
        assert(len(transparencies) == gtm_args.get_zoom_levels()), \
            "There should be as many transparencies arrays as zoom levels"
        len_zoom_0 = len(transparencies[0])
        for zoom in range(0, len(transparencies)):
            assert len(transparencies[zoom]) == len_zoom_0, \
                "The array with the edge transparencies should have same len across all zooms"
            for i in range(0, len(transparencies[zoom])):
                assert transparencies[zoom][i] >= gtm_args.get_min_transparency(), \
                    "One transparency value was less than the minimum"
                assert transparencies[zoom][i] <= gtm_args.get_max_transparency(), \
                    "One transèarency value was greater than the maximum"









