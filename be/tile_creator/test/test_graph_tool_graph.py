import os
import unittest
import numpy as np
import pandas as pd
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.metadata.token_graph_metadata import TokenGraphMetadata
from be.tile_creator.src.new_way.test.fixtures import TEST_DATA
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from commands.gtm import getFinalConfigurations


class TestGraphToolGraph(unittest.TestCase):
    graph = None
    layout = None
    gtg = None

    @classmethod
    def setUpClass(cls):
        if not os.getcwd().split('/')[-1] == 'tokengallery':
            os.chdir(os.path.abspath(os.path.join(os.getcwd(), 'tokengallery')))
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})
        defaultConfig = getFinalConfigurations({'--csv': TEST_DATA},  "test_graph")
        cls.layout = VisualLayout(cls.graph, defaultConfig)
        cls.transparencyCalculators = TransparencyCalculator(cls.layout.max - cls.layout.min, defaultConfig)
        cls.layout.edgeTransparencies = cls.transparencyCalculators.calculateEdgeTransparencies(
            cls.layout.edgeLengths)
        cls.layout.vertexShapes = ['inactive_fake'] * len(cls.layout.vertexSizes)
        metadata = TokenGraphMetadata(cls.graph, cls.layout, defaultConfig)
        cls.gtg = GraphToolTokenGraph(cls.graph.edge_ids_to_amount,
                                      cls.layout,
                                      metadata,
                                      defaultConfig['curvature'])

    def test_init(cls):
        cls.assertIsNotNone(cls.gtg)

    def test_edge_curvature_is_negative(cls):
        """
        Has to be  negative because we set the curvature for outgoing edges.
        Negative curvature means that the curvature will be clockwise wrt to source to target.
        We require that following the edge clockwise points to the direction of the transfer.
        :return:
        """
        cls.assertLess(cls.gtg.edgeCurvature, 0)

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

        def extractEdgesFromGtGraph():
            edgesGraphTool = list(cls.gtg.g.edges())
            edgesListOfLists = list(map(lambda e: [int(e.source()), int(e.target())], edgesGraphTool))
            edgesNumpy2d = np.array(edgesListOfLists)
            edgesPandas = pd.DataFrame(edgesNumpy2d).rename(columns={0: 'source', 1: 'target'})
            return edgesPandas

        graphToolEdges = extractEdgesFromGtGraph()
        # by definition we order the edges PRIMARILY on the source vertex id
        cls.assertTrue(graphToolEdges['source'].is_monotonic)
        #  we order the edges secondarily on target id,
        # here we group each target vertex by source, then each of those subgroups of targets should be monotonically  increasing
        cls.assertTrue(graphToolEdges.groupby(by='source').target.is_monotonic_increasing.all())
