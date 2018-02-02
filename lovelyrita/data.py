from __future__ import print_function
import numpy as np
import pandas as pd

column_map = {'street': 'street',
              'city': 'city',
              'state': 'state',
              'Ticket Number': 'ticket_number',
              'Ticket Issue Date': 'ticket_issue_date',
              'Ticket Issue Time': 'ticket_issue_time',
              'Violation External Code': 'violation_external_code',
              'Violation Desc Long': 'violation_desc_long',
              'Street No': 'street_no',
              'Street Name': 'street_name',
              'Street Suffix': 'street_suffix',
              'Fine Amount': 'fine_amount',
              'Badge #': 'badge_number'}

def read_data(paths, dtype, column_map=column_map, delimiter=','):
    """Load data from a list of file paths.

    Parameters
    ----------
    paths : list
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
    if isinstance(paths, (tuple, list)):
        paths = [paths,]

    if column_map is None:
        usecols = None
    else:
        usecols = column_map.keys()
    df = pd.concat([pd.read_csv(path, usecols=usecols,
                                delimiter=delimiter)
                    for path in paths])
    df = df.reset_index(drop=True)

    if column_map:
        df.rename(columns=column_map, inplace=True)

    return df
