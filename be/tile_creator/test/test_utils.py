import os
import unittest
from be.tile_creator.src.new_way.test.fixtures import IMG_SIMILARITY_DIR

from be.utils import compareImages, isImage


class TestUtils(unittest.TestCase):


    def setUp(self) -> None:
        self.differentThreshold = 0.5
        self.similarThreshold = 0.72


    # TODO test other utils

    def test_compare_images(self):
        """
        Test that the method to compare imgs performs as expected on a known test set
        :return:
        """
        dirs = [os.path.join(IMG_SIMILARITY_DIR, path) for path in os.listdir(IMG_SIMILARITY_DIR) if os.path.isdir(path)]
        for dir in dirs:
            files = [os.path.join(dir, path) for path in os.listdir(dir) if isImage(path)]
            yes_scores = []
            no_scores = []
            for img1 in files:
                for img2 in files:
                    similarityScore = compareImages(img1, img2)
                    comparingYesInstances = 'yes' in img1 and 'yes' in img2
                    comparingNoInstances = 'no' in img1 and 'no' in img2
                    comparingTheSameNoInstance = img1 == img2
                    comparingYesVsNo = not comparingYesInstances and not comparingNoInstances
                    if comparingYesInstances or comparingTheSameNoInstance:
                        yes_scores.append(similarityScore)
                        if similarityScore < self.similarThreshold:
                            # print("similarity({0}, {1}) < {2}".format(img1, img2, similarity_score))
                            self.assertGreater(similarityScore, self.similarThreshold,
                                               "similarity({0}, {1}) < {2}".format(img1, img2, self.similarThreshold))
                    elif comparingYesVsNo:
                        no_scores.append(similarityScore)
                        if similarityScore > self.differentThreshold:
                            # print("similarity({0}, {1}) > {2}".format(img1, img2, similarity_score))
                            self.assertLess(similarityScore, self.differentThreshold,
                                            "similarity({0}, {1}) > {2}".format(img1, img2, self.differentThreshold))
            # print(min(yesScores))
            # print(max(no_scores))