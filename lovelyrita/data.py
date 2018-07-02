from __future__ import print_function
import numpy as np
import pandas as pd
from shapely.geometry import Point
import geopandas
from lovelyrita.clean import clean as clean_data
from lovelyrita.config import VALID_COLUMN_NAMES as valid_column_names


def read_data(paths, usecols=None, delimiter=',', clean=False):
    """Load data from a list of file paths.

    Parameters
    ----------
    paths : list
        A list of file paths to the data to be loaded
    usecols : list of str
        If provided, only load these columns
    dtype : dict
        A dict containing key (column name) and value (data type)
    delimiter : str

    Returns
    -------
    A DataFrame containing the loaded data
    """
    if not isinstance(paths, (tuple, list)):
        paths = [paths, ]

    dataframe = []
    for path in paths:

        if usecols is None:
            usecols = get_column_names(path)

        df = pd.read_csv(path, usecols=usecols, delimiter=delimiter)

        df['street'] = df['street'].str.strip(' ')

        if clean:
            df = clean_data(df)

        dataframe.append(df)

    dataframe = pd.concat(dataframe).reset_index(drop=True)

    return dataframe


def get_column_names(path, valid_column_names=valid_column_names):
    """Return the intersection of columns present in the dataset and valid column names

    Parameters:
    -----------
    path : str
    valid_column_names : list of st

    Return:
    -------
    """
    column_names = pd.read_csv(path, nrows=1)
    return [n for n in column_names if n in valid_column_names]


def to_geodataframe(dataframe, copy=False, drop_null_geometry=True,
                    projection='epsg:4326'):
    """Convert a pandas DataFrame to geopandas DataFrame.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Must contain latitude and longitude fields
    copy : bool
    drop_null_geometry : bool
    projection : str

    Returns
    -------
    A GeoDataFrame of the given DataFrame
    """
    if copy:
        df = dataframe.copy()
    else:
        df = dataframe

    df.latitude = df.latitude.astype('float32')
    df.longitude = df.longitude.astype('float32')

    points = []
    for x, y in zip(df.latitude, df.longitude):
        if not x == 0:
            points.append(Point(y, x))
        else:
            points.append(None)
    df['geometry'] = points

    df.drop(['latitude', 'longitude'], axis=1, inplace=True)

    if drop_null_geometry:
        df = df.loc[~df.geometry.isnull()]

    # geopandas cannot handle datetime formats, so convert to string
    for column in df.select_dtypes(include=['datetime']):
        df[column] = df[column].dt.strftime('%m/%d/%y %H:%M:%S')

    return geopandas.GeoDataFrame(df, geometry='geometry', crs={'init': projection})


def write_shapefile(geodataframe, path):
    """Write a geodataframe to a shapefile.

    Parameters
    ----------
    geodataframe : geopandas.GeoDataFrame
    path : str
    """
    geodataframe.to_file(path, driver='ESRI Shapefile')


def get_sample_value(series):
    """Return a sample value from a series

    Parameters
    ----------
    series : pandas.Series

    Returns
    -------
    A sample value from the series or None if all values in the series are null
    """
    unique = series.unique()
    for value in unique:
        if value is not np.nan:
            return value


def summarize(dataframe):
    """Generate a summary of the data in a dataframe.

    Parameters
    ----------
    dataframe : pandas.DataFrame

    Returns
    -------
    A DataFrame containing the data type, number of unique values, a sample value, number and
    percent of null values
    """
    column_report = []
    for column in dataframe.columns:
        unique = dataframe[column].unique()
        sample = get_sample_value(dataframe[column])
        n_null = dataframe[column].isnull().sum()
        pct_null = 100. * n_null / dataframe.shape[0]
        r = [column, dataframe[column].dtype, len(unique), sample, n_null, pct_null]
        column_report.append(r)

    columns = ["Column Name", "Data Type", "Unique Count", "Sample Value", "null", "% null"]
    column_report = pd.DataFrame(column_report, columns=columns).round(2)
    column_report.sort_values(by="null", inplace=True)

    return column_report
