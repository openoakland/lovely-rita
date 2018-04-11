from six import string_types
import re
import pandas as pd

# use sparingly, these take a lot of time to evaluate
REPLACEMENTS = [(r'^ONE ', '1 '),
                (r'^TWO ', '2 '),
                (' -', '-'),
                (r' TERM$', ' TERMINAL'),
                (r'^#', '')]


VALID_SUFFIXES = ['AVE', 'AVEN', 'BLOCK', 'BLVD', 'BOULEVARD', 'CIR', 'COURT',
                  'CREST', 'CREEK', 'CRK', 'DR', 'DRI', 'DRIVE', 'HBR', 'HTS',
                  'LANE', 'LOOP', 'PARKWAY', 'PKWAY', 'PKWY', 'PL', 'PLACE',
                  'PLAZA', 'PLZ', 'R', 'ROAD', 'SR', 'ST', 'STREET',
                  'TERR', 'TERRACE', 'VISTA', 'VW', 'WAY', 'WY']


def replace(addresses, replacements=REPLACEMENTS, inplace=True):
    """Replace text in addresses

    Parameters
    ----------
    addresses : pandas.Series
    replacements : tuple list of tuples
        Replacements provided as (pattern to replace, replacement). Multiple replacements can be 
        provided as a list of tuples
    inplace : bool

    Returns
    -------
    If inplace is False, returns the address series with the replacements made.
    """
    if isinstance(replacements[0], string_types):
        replacements = [replacements, ]

    if inplace:
        addr = addresses
    else:
        addr = addresses.copy()

    for pattern, replacement in REPLACEMENTS:
        addr.replace(pattern, replacement, regex=True, inplace=True)

    if not inplace:
        return addr


def parse_123_main_street(addresses):
    """Parse the common address format, e.g. 123 MAIN STREET

    Parameter
    ---------
    addresses : pandas.Series

    Returns
    -------
    A DataFrame containing street name and street column for those rows that were successfully 
    parsed
    """
    patt = re.compile(r'^(?P<street_no>\d+\-?\d?) (?P<street_name>[\w\d\s]+)')

    street = addresses.str.extract(patt, expand=True)
    street.dropna(inplace=True)

    return street


def parse_P123_main_street(addresses):
    """Parse addresses that contain a prefix, e.g., P123-1 PARK STREET

    Parameter
    ---------
    addresses : pandas.Series

    Returns
    -------
    A DataFrame containing street name and street column for those rows that were successfully 
    parsed
    """
    patt = re.compile(r'^(?P<prefix>[A-Z]+)\-?(?P<street_number>\d+[\-\W]?\d?) '
                      '(?P<street_name>[\w\d\s]+)')
    street = addresses.str.extract(patt, expand=True)
    street.dropna(inplace=True)

    drop_indices = []
    for i, s in street.iterrows():
        street_words = s.street_name.split(' ')
        drop = True
        for street_word in street_words:
            if street_word.startswith(s.prefix[0]):
                drop = False
        if drop:
            drop_indices.append(i)

    street.drop(drop_indices, inplace=True)

    return street


def parse_addresses(addresses):
    """Parse addresses into street name and number according to several rules.

    Parameter
    ---------
    addresses : pandas.Series

    Returns
    -------
    A DataFrame containing street name and street column for those rows that were successfully 
    parsed
    """
    # Many addresses are in parking lots. Those will not have street numbers, so we should treat them separately. We will only concern ourselves with potential street addresses.

    lot_indices = addresses.str.contains('^[A-Z]LOT.*LOT$')
    street_addresses = addresses.loc[~lot_indices]

    street = pd.DataFrame({'street_name': None, 'street_number': None},
                          index=addresses.index)

    new_street = parse_123_main_street(street_addresses)
    street.update(new_street)

    new_street = parse_P123_main_street(street_addresses)
    street.update(new_street)

    return street


def clean_street_suffixes(street):
    import numpy as np
    import difflib

    candidates = ['AVENUE', 'DRIVE', 'BLOCK', 'PLACE', 'STREET']

    def get_suffix_match(s):
        if isinstance(s, np.float):
            return
        match = difflib.get_close_matches(s, candidates, n=1, cutoff=0.81)
        if len(match) == 1:
            return match[0]
        else:
            return
    street = street.street_suffix.apply(get_suffix_match)

    return street[~pd.isnull(street)]
