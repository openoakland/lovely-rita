from __future__ import print_function
import numpy as np
import pandas as pd


def get_data(data_files, dtype, column_map=None, delimiter=','):
    """Load data from a list of file paths.

    Parameters
    ----------
    data_files : list
        A list of file paths to the data to be loaded
    dtype : dict
        A dict containing key (column name) and value (data type)
    column_map : dict
        A dict containing key, original column name, and value, output column name
    delimiter : str

    Returns
    -------
    A DataFrame containing the loaded data
    """
    df = pd.concat([pd.read_csv(f, dtype=dtype, delimiter=delimiter)
                    for f in data_files])
    df = df.reset_index(drop=True)

    if column_map:
        df.rename(columns=column_map, inplace=True)

    return df

def get_column_report(df):
    """Generate a summary of the data in a DataFrame
    """
    column_report = []
    for column in df.columns:
        unique = df[column].unique()
        sample = np.nan
        for value in unique:
            if value is not np.nan:
                sample = value
                break
        nans = df[column].isnull().sum()
        pct_nan = 100. * nans / df.shape[0]
        column_report.append([column, df[column].dtype, len(unique), sample, nans, pct_nan])

    columns = ["Column Name", "Data Type", "Unique Count",
               "Sample Value", "NaNs", "% NaN"]
    column_report = pd.DataFrame(column_report, columns=columns).round(2)
    column_report.sort_values(by="NaNs", inplace=True)
    return column_report

def get_uniques(df):
    """Return the unique values for each column
    """
    for column in df.columns:
        print(column, df[column].unique())

def get_addresses(df):
    addresses = set()
    for i, item in (df["Street"] + " " +
                    df["City"] + " " +
                    df["State"]).iteritems():
        addresses.add(" ".join(item.lower().split()))

    return list(addresses)

def output_addresses(df, file_out):
    """
    """
    addresses = get_addresses(df)
    with open(file_out, 'w') as output:
        for address in addresses:
            output.write(address + '\n')
    return addresses
