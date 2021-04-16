import numpy as np


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
    original_median = np.median(list(original_values))
    medToMax = max(list(original_values)) - original_median
    medToMax = max(1, medToMax)
    targetMedToMax = target_max - target_median
    shifted_values = original_values - original_median
    scaled_and_shifted_values = shifted_values * (targetMedToMax / medToMax) + target_median
    scaled_and_shifted_values = np.clip(scaled_and_shifted_values, 1, target_max)
    return scaled_and_shifted_values
