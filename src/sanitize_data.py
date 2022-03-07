'''
Xavier Beech
CSE163
Set of methods for sanitizing CSV datasets from public use data files from
the National Science Foundation's Survey of Science and Engineering Research
Facilities. Dataset information can be found in
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


def filter_df(df, filter_title, filter_val='1', valid_columns=None):
    '''
    Filters DataFrame for columns where the value at
    (valid_columns, filter_title) equals filter_val, and returns.
    If valid_columns equals None, filters for all columns.
    Note: currently only works for valid_columns == None,
    if not, returns identical DataFrame. Will remove
    non-None functionality and revise if not needed
    by release.
    '''
    data = df
    if valid_columns is None:
        data = data[data[filter_title] == filter_val]
    # else:
    #   for collumn in valid_columns:
    #       data.loc[data[filter_title] == filter_val, filter_title] = np.nan
    return data


def export_to_csv(df, file_path):
    '''
    Exports DataFrame to CSV.
    Handles non-existent parent diretories and relative paths.
    '''
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path)
    print('Export Successful!')


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
    # why they'd include non-Y answers in the dataset, but we have to filter
    # for them just in case.
    data = filter_df(data, 'SUBMISSION_FLAG', 'Y')
    # Added functionality that is not currently needed (or working).
    # Will probably be removed for final release. Associated with
    # RRBOX and on in FILTER_VALUES[2019] (more info in Constants.py)
    # for val in FILTER_VALUES[year].keys():
    #     data = filter_df(
    #         data, val, FILTER_VALUES[year][val][0],
    #         FILTER_VALUES[year][val][1:])
    #
    data = data.replace('S', 0)
    export_to_csv(data, location)


if __name__ == '__main__':
    main()
