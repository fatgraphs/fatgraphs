import os
import unittest

from be.tile_creator.test.constants import IMG_SIMILARITY_DIR
from be.utils import compare_images, is_image


class TestUtils(unittest.TestCase):


    def setUp(self) -> None:
        self.different_threshold = 0.72
        self.similar_threshold = 0.45

    def test_compare_images(self):
        """
        Test that the method to compare imgs performs as expected on a known test set
        :return:
        """
        files =  [os.path.join(IMG_SIMILARITY_DIR, path) for path in os.listdir(IMG_SIMILARITY_DIR) if is_image(path)]
        yes_scores = []
        no_scores = []
        for img1 in files:
            for img2 in files:
                similarity_score = compare_images(img1, img2)
                comparing_yes_instances = 'yes' in img1 and 'yes' in img2
                comparing_the_same_no_instance = img1 == img2
                if comparing_yes_instances  or comparing_the_same_no_instance:
                    yes_scores.append(similarity_score)
                    self.assertGreater(similarity_score, self.similar_threshold,
                                       "similarity({0}, {1}) < {2}".format(img1, img2, self.similar_threshold))
                else:
                    no_scores.append(similarity_score)
                    self.assertLess(similarity_score, self.different_threshold,
                                    "similarity({0}, {1}) > {2}".format(img1, img2, self.different_threshold))
