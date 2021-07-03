import math

import cv2
import numpy as np
from PIL import Image
from numba import jit

ASCII_N = 110


def shift_and_scale(original_values, target_median, target_max):
    """
    Scales a list of values to a new range.
    :param original_values: list-like object of values that we intend to scale to a different range
    :param target_median: the values will be scaled to a new range that has this median
    :param target_max: the values will be scaled to a new range that has this max value
    :return:


    example:
    > shift_and_scale([1,2,3,4,5,6,7,8,9], 10, 20)
    > [ 1, 2.5, 5, 7.5, 10. 12.5, 15, 17.5, 20 ]

    """

    original_values = list(original_values)

    original_median = np.median(original_values)
    medToMax = max(list(original_values)) - original_median
    medToMax = max(1, medToMax)
    targetMedToMax = target_max - target_median
    shifted_values = original_values - original_median
    scaled_and_shifted_values = shifted_values * (targetMedToMax / medToMax) + target_median
    # TODO define a better minimum
    MINIMUM = 0.000001
    # if MINIMUM > target_max:
    #     raise Exception("Minimum is greater than target_max, something is wrong.")
    scaled_and_shifted_values = np.clip(scaled_and_shifted_values, MINIMUM, max(2, target_max))
    return scaled_and_shifted_values


@jit(nopython=True)
def gauss(x, mean, std, min_out=0, max_out=1):
    """
    :param x: input value of the gaussian function
    :param mean: the center of the gaussian bell
    :param std: the standard deviation, larger values make the gaussian more flat
    :param min_out: ensures that the output is >= min_clip
    :param max_out: ensures that the output is <= min_clip
    :return: computes the gaussian value of the provided x value scaled to fit within min and max if provided
    """
    return (max_out - min_out) * math.e ** ((-1 * ((x - mean) ** 2.)) / (2 * (std ** 2.))) + min_out


def calculate_diagonal_square_of_side(side):
    """
    :param side: a square with this side length
    :return: the length of the diagonal
    """
    return math.sqrt(side ** 2 + side ** 2)


def find_index_of_nearest(array, value):
    """
    :param array: array of values
    :param value: a target value
    :return: the index in the array corresponding to the element closest to the target value
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return int(idx)


def compare_images(img_1_path, img_2_path):
    """
    Compares two images and returns a similarity score: 1 means they are the same,
    0 means they are completely different.
    Note that the images should be of the same size for this to work as intended.
    :param img_1_path:
    :param img_2_path:
    :return: score between 0 and 1
    """
    img1 = cv2.imread(img_1_path) if isinstance(img_1_path, type("string")) else img_1_path
    img2 = cv2.imread(img_2_path) if isinstance(img_2_path, type("string")) else img_2_path
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()

    # detect keypoints and descriptors
    kp_a, desc_a = orb.detectAndCompute(img1, None)
    kp_b, desc_b = orb.detectAndCompute(img2, None)

    # define the bruteforce matcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # perform matches.
    matches = bf.match(desc_a, desc_b)
    # Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
    similar_regions = [i for i in matches if i.distance < 45]
    if len(matches) == 0:
        return 0
    return len(similar_regions) / len(matches)


def is_image(filename):
    """

    :param filename: a file name, either a full path or just the file name
    :return: true/false  depending if the provided filename ends with a known image extension
    """
    f = filename.lower()
    return f.endswith(".png") or f.endswith(".jpg") or \
           f.endswith(".jpeg") or f.endswith(".bmp") or \
           f.endswith(".gif") or '.jpg' in f or f.endswith(".svg")


def concat_horizontally(im1, im2):
    """
    :param im1:
    :param im2:
    :return: horizontal concatenation of the 2 input images
    """
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def concat_vertically(imgOrPath1, imgOrPath2):
    """
    :param im1:
    :param im2:
    :return: vertical concatenation of the 2 input images
    """

    def _concatv(im1, im2):
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

    if isinstance(imgOrPath1, type("string")) and isinstance(imgOrPath2, type("string")):
        with Image.open(imgOrPath1) as img1, Image.open(imgOrPath2) as img2:
            return _concatv(img1, img2)
    else:
        return _concatv(imgOrPath1, imgOrPath2)


def concat_horizontally(imgOrPath1, imgOrPath2):
    """
    :param im1:
    :param im2:
    :return: vertical concatenation of the 2 input images
    """

    def _concath(im1, im2):
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    if isinstance(imgOrPath1, type("string")) and isinstance(imgOrPath2, type("string")):
        with Image.open(imgOrPath1) as img1, Image.open(imgOrPath2) as img2:
            return _concath(img1, img2)
    else:
        return _concath(imgOrPath1, imgOrPath2)


def scale_square(imgOrPath, side, scaled_img=None):
    """
    :param imgOrPath: path of input image
    :param side: desired length of the output side
    :param name: 
    :return: 
    """

    def _scale(img):
        wpercent = (side / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        scaled_img = img.resize((side, hsize), Image.ANTIALIAS)
        return scaled_img

    if isinstance(imgOrPath, type("string")):
        with Image.open(imgOrPath) as img:
            return _scale(img)
    else:
        return _scale(imgOrPath)


def merge_tiles(tiles):
    row1 = concat_vertically(tiles[0], tiles[1])
    row2 = concat_vertically(tiles[2], tiles[3])
    return concat_horizontally(row1, row2)


def to_cv(pilImage):
    open_cv_image = np.array(pilImage)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image


def wkt_to_x_y_list(wkt):
    """

    :param wkt: well known text representation of a 2D POINT (a point in GIS).
            e.g. POINT(34234 42)
    :return: a python list where the first element is the x and the second is the y
    """
    p = wkt.split('(')[-1].split(')')[0].split(' ')
    return [float(p[0]), float(p[1])]


def convert_graph_coordinate_to_map(source_x, source_y, target_x, target_y,
                                    source_x_pixel, source_y_pixel, target_x_pixel, target_y_pixel,
                                    tile_size, min_coordinate, max_coordinate):
    """
    This function is specifically written to work with Rapids apply method: the apply method applies an operation
    on a GPU frame row by row.
    """
    graph_side = max_coordinate - min_coordinate
    for i, (xs, ys, xt, yt) in enumerate(zip(source_x, source_y, target_x, target_y)):
        scaling_factor = tile_size / graph_side
        source_x_pixel[i] = (xs + abs(min_coordinate)) * scaling_factor
        source_y_pixel[i] = (ys + abs(min_coordinate)) * scaling_factor
        target_x_pixel[i] = (xt + abs(min_coordinate)) * scaling_factor
        target_y_pixel[i] = (yt + abs(min_coordinate)) * scaling_factor