'''
Xavier Beech
CSE163
Sanitizes the National Science Foundation's Survey of
Science and Engineering Research Facilities.
Dataset information can be found in
./raw_data/2019-faciliities-puf-user-guide.pdf
'''
from pathlib import Path
import sys
from os.path import abspath
import pandas as pd
from Constants import NASF_COLUMNS, GENERAL_COLUMNS, FILTER_VALUES
# import numpy as np


''' call using this syntax in terminal:
    [python executable] [path of sanitize_data.py] \
        [path of desired CSV to sanitize] [year]\
            [path of desired location and name of CSV]
    ex:./.env/python.exe ./src/sanitize_data.py \
        ./raw_data/facilities_2019_imputed.csv ./data/2019_sanitized.csv 2019
'''


def main():
    '''
    Handles main chunk of data sanitization, including initialization and
    path handling. Returns sanitized file. Currently uses hardcoded settings,
    however it would be nice to at some point revise it for
    argument-set instead. Pulls column names on a year-by-year basis
    from Constants.py
    '''
    # Basic argument handling and reporting back to user for debug purposes.
    origin_path, location, year = sys.argv[1:]
    origin_path = abspath(origin_path)
    location = abspath(location)
    year = int(year)
    print('Data File Path:', origin_path)
    print('Location Path: ', location)
    print('Year: ', year)

    # Reads data from CSV, and then retrieves and aggregates into single list.
    data = pd.read_csv(origin_path, encoding='ISO-8859-1')
    valid_columns = [GENERAL_COLUMNS[year], NASF_COLUMNS[year]]
    valid_columns.extend(FILTER_VALUES[year].keys())
    # Iterates through keys of FILTER_VALUES and adds all values to
    # list of valid_columns.
    valid_columns.extend(map(lambda x: FILTER_VALUES[year][x][1:],
                             FILTER_VALUES[year].keys()))
    # Since FILTER_VALUES is a dictionary of list-of-lists with years as keys,
    # once the values (list-of-lists) have been added they must then be
    # unpacked to create a single list of Strings. More info in Constants.py.
    valid_columns = [item for sublist in valid_columns for item in sublist]
    # Now that a list of all columns we want to keep has been assembled,
    # we can finally cut the dataset down to only those columns.
    data = data.filter(items=valid_columns)
    # Filters only for values which have responses. Frankly I'm not sure
    # why they'd include non-Y answers in the dataset.
    data = data[data['SUBMISSION_FLAG'] == 'Y'].drop(
        labels='SUBMISSION_FLAG', axis=1)
    data = data.replace('S', 0)
    Path(location).parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(location)
    print('Export Successful!')


if __name__ == '__main__':
    main()
