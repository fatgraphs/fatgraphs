import os
import unittest

from skimage.metrics import structural_similarity

from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.src.token_graph_metadata import TokenGraphMetadata
from be.tile_creator.test.constants import TEST_DATA_DIR, TEST_DIR, TEST_OUTPUT_DIR, TEST_REFERENCE_OUTPUT_DIR
from be.utils import compare_images
from gtm import get_final_configurations
from PIL import Image
# import the necessary packages
import matplotlib.pyplot as plt
import numpy as np
# import cv2

class TestRenderer(unittest.TestCase):

    graph = None
    layout = None
    gtg = None
    transparency_calculator = None
    tile_renderer = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA_DIR, {'dtype': {'amount': object}})
        default_config = get_final_configurations({'--csv': TEST_DATA_DIR}, TEST_OUTPUT_DIR, "test_graph")
        cls.layout = VisualLayout(cls.graph, default_config)
        metadata = TokenGraphMetadata(cls.graph, cls.layout, default_config)
        cls.gtg = GraphToolTokenGraph(cls.graph.edge_ids_to_amount,
                                      cls.layout,
                                      metadata,
                                      default_config['curvature'])
        cls.transparency_calculators = TransparencyCalculator(cls.layout.max - cls.layout.min, default_config)
        cls.layout.edge_transparencies = cls.transparency_calculators.calculate_edge_transparencies(cls.layout.edge_lengths)
        cls.tile_renderer = TilesRenderer(cls.gtg, cls.layout.edge_transparencies, metadata, cls.transparency_calculators, default_config)

    def test_initialisation(cls):
        cls.assertIsNotNone(cls.tile_renderer)

    def test_it_can_render(cls):
        cls.tile_renderer.render()

    def test_test_output_is_similar_to_reference(cls):
        image_one = Image.open(os.path.join(TEST_OUTPUT_DIR, 'test1.png'))
        image_two = Image.open(os.path.join(TEST_OUTPUT_DIR, 'test2.png'))
        im1 = np.array(image_one.getdata()).reshape((256, 256, 3))
        im2 = np.array(image_two.getdata()).reshape((256, 256, 3))
        compare_images(im1, im2, "yest")
        delta = compare_images(image_one, image_two)
        cls.assertLess(delta, 1.5)

        image_one = cv2.imread(os.path.join(TEST_OUTPUT_DIR, 'z_0x_0y_0.png'))
        image_two = cv2.imread(os.path.join(TEST_REFERENCE_OUTPUT_DIR, 'z_0x_0y_0.png'))
        image_one = cv2.cvtColor(image_one, cv2.COLOR_BGR2GRAY)
        image_two = cv2.cvtColor(image_two, cv2.COLOR_BGR2GRAY)


