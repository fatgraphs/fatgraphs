import unittest
import numpy as np
from numpy.random import randint

from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.new_way.test.fixtures import TEST_DATA, TEST_DIR
from be.tile_creator.src.render.edge_distribution_plot_renderer import EdgeDistributionPlotRenderer
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.utils import calculateDiagonalSquareOfSide
from be.gtm import getFinalConfigurations


class TestRenderer(unittest.TestCase):
    SIDE_GRAPH = 100
    LONGEST = int(calculateDiagonalSquareOfSide(SIDE_GRAPH))
    TILE_SIZE = 256
    transparencyCalculator = None
    plotRenderer = None
    layout = None

    @classmethod
    def setUpClass(cls):
        defaultConfig = getFinalConfigurations({'--csv': TEST_DATA, '-z': 4},
                                                 "test_graph")

        attr = getattr(defaultConfig, 'outputFolder', None)
        cls.assertIsNone(cls, attr)
        defaultConfig['output_folder'] = TEST_DIR


        cls.transparencyCalculator = TransparencyCalculator(cls.SIDE_GRAPH, defaultConfig)
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})
        fakeEdges = randint(1, cls.LONGEST, 200)
        fakeEdges = np.append(fakeEdges, cls.LONGEST)
        cls.layout = VisualLayout(cls.graph, defaultConfig)
        cls.layout.edgeTransparencies = cls.transparencyCalculator.calculateEdgeTransparencies(
            cls.layout.edgeLengths)
        cls.plotRenderer = EdgeDistributionPlotRenderer(defaultConfig, cls.layout)

    def testInitialisation(cls):
        cls.assertIsNotNone(cls.transparencyCalculator)
        cls.assertIsNotNone(cls.plotRenderer)

    def testItProducesPlotImgs(cls):
        cls.plotRenderer.render()
