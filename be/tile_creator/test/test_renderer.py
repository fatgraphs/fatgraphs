
import unittest

from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.new_way.test.fixtures import TEST_DATA, TEST_DIR
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.src.metadata.token_graph_metadata import TokenGraphMetadata
from commands.gtm import getFinalConfigurations


class TestRenderer(unittest.TestCase):
    graph = None
    layout = None
    gtg = None
    transparencyCalculator = None
    tileRenderer = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})
        defaultConfig = getFinalConfigurations({'--csv': TEST_DATA},
                                                  "test_graph")

        attr = getattr(defaultConfig, 'outputFolder', None)
        cls.assertIsNone(cls, attr)
        defaultConfig['output_folder'] = TEST_DIR

        cls.layout = VisualLayout(cls.graph, defaultConfig)
        metadata = TokenGraphMetadata(cls.graph, cls.layout, defaultConfig)
        cls.transparencyCalculators = TransparencyCalculator(cls.layout.max - cls.layout.min, defaultConfig)
        cls.layout.edgeTransparencies = cls.transparencyCalculators.calculateEdgeTransparencies(
            cls.layout.edgeLengths)
        cls.layout.vertexShapes = ['inactive_fake'] * len(cls.layout.vertexSizes)
        cls.gtg = GraphToolTokenGraph(cls.graph.edge_ids_to_amount,
                                      cls.layout,
                                      metadata,
                                      defaultConfig['curvature'])

        cls.tileRenderer = TilesRenderer(cls.gtg,  metadata, defaultConfig)

    def test_initialisation(cls):
        cls.assertIsNotNone(cls.tileRenderer)

    def test_it_can_render(cls):
        cls.tileRenderer.renderGraph()

    # def test_test_output_is_similar_to_reference(cls):
    #
    #     def prepareTiles(imgs):
    #         tilesZoom1 = imgs[1:5]
    #         tilesZoom1.reverse()
    #         zoom1 = mergeTiles(tilesZoom1)
    #         zoom1 = toCv(zoom1)
    #         return imgs[0], zoom1
    #
    #     referenceImgsPaths = [os.path.join(TEST_REFERENCE_OUTPUT_DIR, path) for path in
    #                             os.listdir(TEST_REFERENCE_OUTPUT_DIR) if isImage(path)]
    #     currentImgsPaths = [os.path.join(TEST_OUTPUT_DIR, path) for path in os.listdir(TEST_OUTPUT_DIR) if
    #                           isImage(path)]
    #
    #     referenceImgs = prepareTiles(referenceImgsPaths)
    #     currentImgs = prepareTiles(currentImgsPaths)
    #
    #     cls.assertEqual(len(referenceImgs), len(currentImgs),
    #                     "There are mismatching numbers of tiles in the reference folder and current output")
    #     zipped = zip(referenceImgs, currentImgs)
    #     for (a, b) in zipped:
    #         score = compareImages(a, b)
    #         if score > 0.7:
    #             print("The algorithm has automatically determined that the current output is similar to the reference output")
    #             cls.assertTrue(True)
    #         else:
    #             a = cv2.imread(a) if isinstance(a, type("string")) else a
    #             b = cv2.imread(b) if isinstance(b, type("string")) else b
    #             height = a.shape[0]
    #             width = a.shape[1]
    #             side_by_side = np.concatenate((a, b), axis=1)
    #             cv2.line(side_by_side, (width, 0), (width, height), (255, 0, 0), 2)
    #             cv2.imshow("Manual intervention required.\nPress n if the imgs look different, any key if it's okay",
    #                        side_by_side)
    #             key = cv2.waitKey(0)
    #             if key == ASCII_N:
    #                 cls.assertTrue(False,
    #                                "You have manually decided that the current output is different from the reference output")
