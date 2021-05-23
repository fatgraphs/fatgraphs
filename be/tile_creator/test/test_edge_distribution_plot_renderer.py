import os
import unittest
import cv2
import numpy as np
from numpy.random import randint

from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.render.edge_distribution_plot_renderer import EdgeDistributionPlotRenderer
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.src.token_graph_metadata import TokenGraphMetadata
from be.tile_creator.test.constants import TEST_DATA, TEST_OUTPUT_DIR, TEST_REFERENCE_OUTPUT_DIR, TEST_DIR
from be.utils import compare_images, is_image, ASCII_N, merge_tiles, to_cv, calculate_diagonal_square_of_side
from gtm import get_final_configurations


class TestRenderer(unittest.TestCase):
    SIDE_GRAPH = 100
    LONGEST = int(calculate_diagonal_square_of_side(SIDE_GRAPH))
    TILE_SIZE = 256
    transparency_calculator = None
    plot_renderer = None

    @classmethod
    def setUpClass(cls):
        config = get_final_configurations({'--csv': TEST_DATA, '-z': 4},
                                          TEST_DIR, "test_graph")
        cls.transparency_calculator = TransparencyCalculator(cls.SIDE_GRAPH, config)
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})
        # fake_edges = list(range(0, cls.LONGEST))
        fake_edges = randint(1, cls.LONGEST, 200)
        fake_edges = np.append(fake_edges, cls.LONGEST)
        cls.plot_renderer = EdgeDistributionPlotRenderer(4,
                                                         fake_edges,
                                                         cls.transparency_calculator,
                                                         TEST_DIR,
                                                         cls.SIDE_GRAPH,
                                                         cls.TILE_SIZE)

    def test_initialisation(cls):
        cls.assertIsNotNone(cls.transparency_calculator)
        cls.assertIsNotNone(cls.plot_renderer)

    def test_it_produces_plot_imgs(cls):
        cls.plot_renderer.render()

