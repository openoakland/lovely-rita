import numpy as np

import time
from datetime import datetime

def impute_missing_times(datetimes):
    """Fill in missing times by interpolating surrounding times

    Parameters
    ----------
    datetimes : pandas.Series

    Returns
    -------
    The original Series with missing times replaced by interpolated times
    """
    
    # get valid start and stop indices for null ranges
    n_rows = len(datetimes)

    null_indices = datetimes.isnull().nonzero()[0]

    # remove all but first in consecutive sequences of nulls
    valid_starts = null_indices[1:][np.diff(null_indices)>1]
    if null_indices[0] > 0:
        valid_starts = np.r_[null_indices[0], valid_starts]
    valid_starts -= 1

    # remove all but final in consecutive sequences of nulls
    valid_ends = null_indices[:-1][np.diff(null_indices)>1]
    if null_indices[-1] < (n_rows-1):
        valid_ends = np.r_[valid_ends, null_indices[-1]]
    valid_ends += 1
    
    for valid_start, valid_end in zip(valid_starts, valid_ends):
        start_datetime = datetimes[valid_start]
        end_datetime = datetimes[valid_end]

        start_seconds = time.mktime(start_datetime.timetuple())
        end_seconds = time.mktime(end_datetime.timetuple())

        n = valid_end - valid_start + 1
        interpolated_seconds = np.linspace(start_seconds, end_seconds, n)
        interpolated_datetimes = [datetime.fromtimestamp(s) for s in interpolated_seconds]
        datetimes.iloc[valid_start+1:valid_end] = interpolated_datetimes[1:-1]

    return datetimes
