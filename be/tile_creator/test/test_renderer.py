import os
import unittest
import cv2
import numpy as np

from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.metadata.verticeslabels import VerticesLabels
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.src.metadata.token_graph_metadata import TokenGraphMetadata
from be.tile_creator.test.constants import TEST_DATA, TEST_OUTPUT_DIR, TEST_REFERENCE_OUTPUT_DIR
from be.utils.utils import compare_images, is_image, ASCII_N, merge_tiles, to_cv
from gtm import get_final_configurations


class TestRenderer(unittest.TestCase):
    graph = None
    layout = None
    gtg = None
    transparency_calculator = None
    tile_renderer = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})
        default_config = get_final_configurations({'--csv': TEST_DATA},
                                                  TEST_OUTPUT_DIR,
                                                  "test_graph")
        cls.layout = VisualLayout(cls.graph, default_config)
        vertices_labels = VerticesLabels(default_config, cls.graph.address_to_id, cls.layout.vertex_positions)
        metadata = TokenGraphMetadata(cls.graph, cls.layout, default_config, vertices_labels)
        cls.gtg = GraphToolTokenGraph(cls.graph.edge_ids_to_amount,
                                      cls.layout,
                                      metadata,
                                      default_config['curvature'])
        cls.transparency_calculators = TransparencyCalculator(cls.layout.max - cls.layout.min, default_config)
        cls.layout.edge_transparencies = cls.transparency_calculators.calculate_edge_transparencies(
            cls.layout.edge_lengths)
        cls.tile_renderer = TilesRenderer(cls.gtg, cls.layout, metadata,
                                          cls.transparency_calculators, default_config)

    def test_initialisation(cls):
        cls.assertIsNotNone(cls.tile_renderer)

    def test_it_can_render(cls):
        cls.tile_renderer.render()

    def test_test_output_is_similar_to_reference(cls):

        def _prepare_tiles(imgs):
            tiles_zoom_1 = imgs[1:5]
            tiles_zoom_1.reverse()
            zoom_1 = merge_tiles(tiles_zoom_1)
            zoom_1 = to_cv(zoom_1)
            return imgs[0], zoom_1

        reference_imgs_paths = [os.path.join(TEST_REFERENCE_OUTPUT_DIR, path) for path in
                                os.listdir(TEST_REFERENCE_OUTPUT_DIR) if is_image(path)]
        current_imgs_paths = [os.path.join(TEST_OUTPUT_DIR, path) for path in os.listdir(TEST_OUTPUT_DIR) if
                              is_image(path)]

        reference_imgs = _prepare_tiles(reference_imgs_paths)
        current_imgs = _prepare_tiles(current_imgs_paths)

        cls.assertEqual(len(reference_imgs), len(current_imgs),
                        "There are mismatching numbers of tiles in the reference folder and current output")
        zipped = zip(reference_imgs, current_imgs)
        for (a, b) in zipped:
            score = compare_images(a, b)
            if score > 0.7:
                print("The algorithm has automatically determined that the current output is similar to the reference output")
                cls.assertTrue(True)
            else:
                a = cv2.imread(a) if isinstance(a, type("string")) else a
                b = cv2.imread(b) if isinstance(b, type("string")) else b
                height = a.shape[0]
                width = a.shape[1]
                side_by_side = np.concatenate((a, b), axis=1)
                cv2.line(side_by_side, (width, 0), (width, height), (255, 0, 0), 2)
                cv2.imshow("Manual intervention required.\nPress n if the imgs look different, any key if it's okay",
                           side_by_side)
                key = cv2.waitKey(0)
                if key == ASCII_N:
                    cls.assertTrue(False,
                                   "You have manually decided that the current output is different from the reference output")
