import time
from datetime import datetime
import numpy as np
import pandas as pd
from lovelyrita.addresses import parse_addresses, replace


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
    valid_starts = null_indices[1:][np.diff(null_indices) > 1]
    if null_indices[0] > 0:
        valid_starts = np.r_[null_indices[0], valid_starts]
    valid_starts -= 1

    # remove all but final in consecutive sequences of nulls
    valid_ends = null_indices[:-1][np.diff(null_indices) > 1]
    if null_indices[-1] < (n_rows - 1):
        valid_ends = np.r_[valid_ends, null_indices[-1]]
    valid_ends += 1

    for valid_start, valid_end in zip(valid_starts, valid_ends):
        start_datetime = datetimes.iloc[valid_start]
        end_datetime = datetimes.iloc[valid_end]

        start_seconds = time.mktime(start_datetime.timetuple())
        end_seconds = time.mktime(end_datetime.timetuple())

        n = valid_end - valid_start + 1
        interpolated_seconds = np.linspace(start_seconds, end_seconds, n)
        interpolated_datetimes = [datetime.fromtimestamp(s) for s in interpolated_seconds]
        for i, j in enumerate(range(valid_start + 1, valid_end)):
            datetimes.iloc[j] = interpolated_datetimes[i]

    return datetimes


def find_dollar_columns(dataframe, nrows=100):
    """Find the columns in a DataFrame that contain dollar values
    """
    def is_dollar_series(series):
        if not hasattr(series.iloc[0], 'startswith'):
            return False
        for value in series.iloc[:nrows]:
            if not value.startswith('$'):
                return False
        return True

    return [column for column in dataframe
            if is_dollar_series(dataframe[column])]


def convert_dollar_to_float(dollars):
    return dollars.replace('\$', '', regex=True).astype('float32')


def infer_datetime_format(dt):
    """Infer the datetime format for a Series

    Parameters
    ----------
    dt : pandas.Series

    Returns
    -------
    The datetime format as a string
    """
    datetime_formats = ['%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M']
    for datetime_format in datetime_formats:
        try:
            dt = pd.to_datetime(dt[0], format=datetime_format)
            return datetime_format
        except ValueError:
            pass
    raise Exception('No datetime format detected for {}'.format(dt))


def get_datetime(dataframe):
    """Get a datatime for each row in a DataFrame

    Parameters
    ----------
    dataframe : pandas.DataFrame
        A dataframe with `ticket_issue_date` and `ticket_issue_time` columns

    Returns
    -------
    A Series of datetime values
    """
    dt = dataframe['ticket_issue_date'] + ' ' + dataframe['ticket_issue_time']
    datetime_format = infer_datetime_format(dt)
    return pd.to_datetime(dt, format=datetime_format)


def drop_void(dataframe, inplace=True):
    """Drop voided citations

    Parameters
    ----------
    dataframe : pandas.DataFrame
    inplace : bool

    Returns
    -------
    If `inplace` is False, return the dataframe with voided citations dropped
    """
    void_indices = dataframe.street.str.contains(r'^Z?VOIDZ?')
    null_indices = dataframe.ticket_number.isnull()
    drop_indices = np.logical_or(void_indices, null_indices).nonzero()[0]
    if inplace:
        dataframe.drop(drop_indices, inplace=True)
    else:
        return dataframe.drop(drop_indices, inplace=False)


def clean(dataframe):
    """Apply a series of data cleaning steps to a dataframe of raw data

    Parameters
    ----------
    dataframe : pandas.DataFrame

    Returns
    -------
    A cleaned DataFrame
    """

    drop_void(dataframe)

    replace(dataframe.street)

    addresses = parse_addresses(dataframe.street)
    dataframe.update(addresses)

    dataframe['ticket_issue_datetime'] = get_datetime(dataframe)
    dataframe['ticket_issue_datetime'] = impute_missing_times(dataframe.ticket_issue_datetime)
    dataframe.drop(['ticket_issue_time', 'ticket_issue_date'], axis=1, inplace=True)

    for column in find_dollar_columns(dataframe):
        dataframe[column] = convert_dollar_to_float(dataframe[column])

    return dataframe
