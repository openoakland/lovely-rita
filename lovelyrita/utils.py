from __future__ import print_function
import numpy as np
import pandas as pd


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
