import unittest
import numpy as np
import pandas as pd
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.token_graph_metadata import TokenGraphMetadata
from be.tile_creator.test.constants import TEST_DATA_DIR, TEST_DIR
from gtm import get_final_configurations


class TestGraphToolGraph(unittest.TestCase):

    graph = None
    layout = None
    gtg = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA_DIR, {'dtype': {'amount': object}})
        default_config = get_final_configurations({'--csv': TEST_DATA_DIR}, TEST_DIR, "test_graph")
        cls.layout = VisualLayout(cls.graph, default_config)
        metadata = TokenGraphMetadata(cls.graph, cls.layout, default_config)
        cls.gtg = GraphToolTokenGraph(cls.graph.edge_ids_to_amount,
                                      cls.layout,
                                      metadata,
                                      default_config['curvature'])

    def test_init(cls):
        cls.assertIsNotNone(cls.gtg)

    def test_edge_curvature_is_negative(cls):
        """
        Has to be  negative because we set the curvature for outgoing edges.
        Negative curvature means that the curvature will be clockwise wrt to source to target.
        We require that following the edge clockwise points to the direction of the transfer.
        :return:
        """
        cls.assertLess(cls.gtg.edge_curvature, 0)

    def test_edges_are_in_right_order(cls):
        """
        Edges should be ordered according to the following example, where source is monotonically increasing
        and target is monotonically increasing wrt same source sub-groups
        source  target
        0       99
        1       2
        1       3
        1       5
        2       1
        2       2
        4       100
        """

        def _extract_edges_from_gt_graph():
            edges_graph_tool = list(cls.gtg.g.edges())
            edges_list_of_lists = list(map(lambda e: [int(e.source()), int(e.target())], edges_graph_tool))
            edges_numpy_2d = np.array(edges_list_of_lists)
            edges_pandas = pd.DataFrame(edges_numpy_2d).rename(columns={0: 'source', 1: 'target'})
            return edges_pandas

        graph_tool_edges = _extract_edges_from_gt_graph()
        # by definition we order the edges PRIMARILY on the source vertex id
        cls.assertTrue(graph_tool_edges['source'].is_monotonic)
        #  we order the edges secondarily on target id,
        # here we group each target vertex by source, then each of those subgroups of targets should be monotonically  increasing
        cls.assertTrue(graph_tool_edges.groupby(by='source').target.is_monotonic_increasing.all())



