import math

import numpy as np
import pandas as pd
from numba import jit


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
    MINIMUM = 0.1
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
    return math.sqrt(side**2 + side**2)

def find_index_of_nearest(array, value):
    """
    :param array: array of values
    :param value: a target value
    :return: the index in the array corresponding to the element closest to the target value
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return int(idx)