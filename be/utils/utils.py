import math

import cv2
import numpy as np
from PIL import Image
from numba import jit

ASCII_N = 110


def shiftAndScale(originalValues, targetMedian, targetMax):
    """
    Scales a list of values to a new range.
    :param originalValues: list-like object of values that we intend to scale to a different range
    :param targetMedian: the values will be scaled to a new range that has this median
    :param targetMax: the values will be scaled to a new range that has this max value
    :return:


    example:
    > shiftAndScale([1,2,3,4,5,6,7,8,9], 10, 20)
    > [ 1, 2.5, 5, 7.5, 10. 12.5, 15, 17.5, 20 ]

    """

    originalValues = list(originalValues)

    originalMedian = np.median(originalValues)
    medToMax = max(list(originalValues)) - originalMedian
    medToMax = max(1, medToMax)
    targetMedToMax = targetMax - targetMedian
    shiftedValues = originalValues - originalMedian
    scaledAndShiftedValues = shiftedValues * (targetMedToMax / medToMax) + targetMedian
    # TODO define a better minimum
    MINIMUM = 0.000001
    # if MINIMUM > target_max:
    #     raise Exception("Minimum is greater than target_max, something is wrong.")
    scaledAndShiftedValues = np.clip(scaledAndShiftedValues, MINIMUM, max(2, targetMax))
    return scaledAndShiftedValues


@jit(nopython=True)
def gauss(x, mean, std, minOut=0, maxOut=1):
    """
    :param x: input value of the gaussian function
    :param mean: the center of the gaussian bell
    :param std: the standard deviation, larger values make the gaussian more flat
    :param minOut: ensures that the output is >= minClip
    :param maxOut: ensures that the output is <= minClip
    :return: computes the gaussian value of the provided x value scaled to fit within min and max if provided
    """
    return (maxOut - minOut) * math.e ** ((-1 * ((x - mean) ** 2.)) / (2 * (std ** 2.))) + minOut


def calculateDiagonalSquareOfSide(side):
    """
    :param side: a square with this side length
    :return: the length of the diagonal
    """
    return math.sqrt(side ** 2 + side ** 2)


def findIndexOfNearest(array, value):
    """
    :param array: array of values
    :param value: a target value
    :return: the index in the array corresponding to the element closest to the target value
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return int(idx)


def compareImages(img1Path, img2Path):
    """
    Compares two images and returns a similarity score: 1 means they are the same,
    0 means they are completely different.
    Note that the images should be of the same size for this to work as intended.
    :param img1Path:
    :param img2Path:
    :return: score between 0 and 1
    """
    img1 = cv2.imread(img1Path) if isinstance(img1Path, type("string")) else img1Path
    img2 = cv2.imread(img2Path) if isinstance(img2Path, type("string")) else img2Path
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()

    # detect keypoints and descriptors
    kpA, descA = orb.detectAndCompute(img1, None)
    kpB, descB = orb.detectAndCompute(img2, None)

    # define the bruteforce matcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # perform matches.
    matches = bf.match(descA, descB)
    # Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
    similarRegions = [i for i in matches if i.distance < 45]
    if len(matches) == 0:
        return 0
    return len(similarRegions) / len(matches)


def isImage(filename):
    """

    :param filename: a file name, either a full path or just the file name
    :return: true/false  depending if the provided filename ends with a known image extension
    """
    f = filename.lower()
    return f.endswith(".png") or f.endswith(".jpg") or \
           f.endswith(".jpeg") or f.endswith(".bmp") or \
           f.endswith(".gif") or '.jpg' in f or f.endswith(".svg")


def concatHorizontally(im1, im2):
    """
    :param im1:
    :param im2:
    :return: horizontal concatenation of the 2 input images
    """
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def concatVertically(imgOrPath1, imgOrPath2):
    """
    :param im1:
    :param im2:
    :return: vertical concatenation of the 2 input images
    """

    def concatv(im1, im2):
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

    if isinstance(imgOrPath1, type("string")) and isinstance(imgOrPath2, type("string")):
        with Image.open(imgOrPath1) as img1, Image.open(imgOrPath2) as img2:
            return concatv(img1, img2)
    else:
        return concatv(imgOrPath1, imgOrPath2)


def concatHorizontally(imgOrPath1, imgOrPath2):
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


def scaleSquare(imgOrPath, side, scaledImg=None):
    """
    :param imgOrPath: path of input image
    :param side: desired length of the output side
    :param name: 
    :return: 
    """

    def scale(img):
        wpercent = (side / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        scaledImg = img.resize((side, hsize), Image.ANTIALIAS)
        return scaledImg

    if isinstance(imgOrPath, type("string")):
        with Image.open(imgOrPath) as img:
            return scale(img)
    else:
        return scale(imgOrPath)


def mergeTiles(tiles):
    row1 = concatVertically(tiles[0], tiles[1])
    row2 = concatVertically(tiles[2], tiles[3])
    return concatHorizontally(row1, row2)


def toCv(pilImage):
    openCvImage = np.array(pilImage)
    # Convert RGB to BGR
    openCvImage = openCvImage[:, :, ::-1].copy()
    return openCvImage


def wktToXYList(wkt):
    """

    :param wkt: well known text representation of a 2D POINT (a point in GIS).
            e.g. POINT(34234 42)
    :return: a python list where the first element is the x and the second is the y
    """
    p = wkt.split('(')[-1].split(')')[0].split(' ')
    return [float(p[0]), float(p[1])]


def convertGraphCoordinateToMap(sourceX, sourceY, targetX, targetY,
                                    sourceXPixel, sourceYPixel, targetXPixel, targetYPixel,
                                    tileSize, minCoordinate, maxCoordinate):
    """
    This function is specifically written to work with Rapids apply method: the apply method applies an operation
    on a GPU frame row by row.
    """
    graphSide = maxCoordinate - minCoordinate
    for i, (xs, ys, xt, yt) in enumerate(zip(sourceX, sourceY, targetX, targetY)):
        scalingFactor = tileSize / graphSide
        sourceXPixel[i] = (xs + abs(minCoordinate)) * scalingFactor
        sourceYPixel[i] = (ys + abs(minCoordinate)) * scalingFactor
        targetXPixel[i] = (xt + abs(minCoordinate)) * scalingFactor
        targetYPixel[i] = (yt + abs(minCoordinate)) * scalingFactor