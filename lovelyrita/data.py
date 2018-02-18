from __future__ import print_function
import numpy as np
import pandas as pd

column_map = {"street": 'street',
              "city": 'city',
              "state": 'state',
              "ticket_number": 'ticket_number',
              "ticket_issue_date": 'ticket_issue_date',
              "ticket_issue_time": 'ticket_issue_time',
              "violation_external_code": 'violation_external_code',
              "violation_desc_long": 'violation_desc_long',
              "street_no": 'street_no',
              "street_name": 'street_name',
              "street_suffix": 'street_suffix',
              "fine_amount": 'fine_amount',
              "badge__": 'badge_number'}


def read_data(paths, column_map=column_map, delimiter=','):
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
    if not isinstance(paths, (tuple, list)):
        paths = [paths,]

    if column_map is None:
        usecols = None
    else:
        usecols = column_map.keys()

    df = pd.concat([pd.read_csv(path, dtype='str', usecols=usecols,
                                delimiter=delimiter)
                    for path in paths])
    df = df.reset_index(drop=True)

    df['street'] = df['street'].str.strip(' ')

    if column_map:
        df.rename(columns=column_map, inplace=True)

    return df
