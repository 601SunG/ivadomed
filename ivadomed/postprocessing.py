# Deals with postprocessing on generated segmentation.

import numpy as np
from scipy.ndimage.measurements import label


def threshold_predictions(predictions, thr=0.5):
    """Threshold predictions.

    Threshold a soft (ie not binary) array of predictions given a threshold value, and returns
    a binary array.

    Args:
        predictions (array): array to binarise.
        thr (float): Threshold value: voxels with a value < to thr are assigned 0 as value, 1
            otherwise.
    Returns:
        array: Array containing only zeros or ones.

    """
    thresholded_preds = predictions[:]
    low_values_indices = thresholded_preds < thr
    thresholded_preds[low_values_indices] = 0
    low_values_indices = thresholded_preds >= thr
    thresholded_preds[low_values_indices] = 1
    return thresholded_preds


def keep_largest_object(predictions):
    """Keep the largest connect object.

    Keep the largest connected object from the input array (2 or 3D).
    Note: This function only works for binary segmentation.

    Args:
        predictions (array): Input 2 or 3D binary segmentation.
    Returns:
        array: processed segmentation.

    """
    assert predictions.dtype == np.dtype('int')
    # Find number of closed objects using skimage "label"
    labeled_obj, num_obj = label(predictions)
    # If more than one object is found, keep the largest one
    if num_obj > 1:
        # Keep the largest object
            predictions[np.where(labeled_obj != (np.bincount(labeled_obj.flat)[1:].argmax() + 1))] = 0
    return predictions


def keep_largest_object_2d(predictions, axis=2):
    assert predictions.dtype == np.dtype('int')
    # Split the 3D input array as a list of slice along axis
    list_preds_in = np.split(predictions, predictions.shape[axis], axis=axis)
    # Init list of processed slices
    list_preds_out = []
    # Loop across the slices along the given axis
    for idx in range(len(list_preds_in)):
        slice_processed = keep_largest_object(list_preds_in[idx])
        preds_out.append(slice_processed)
        print(slice_processed.shape, list_preds_in[idx].shape)
    print(predictions.shape, np.stack(list_preds_out, axis=axis).shape)
    return np.stack(list_preds_out, axis=axis)
