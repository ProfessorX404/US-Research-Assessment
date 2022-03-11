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
import pandas as pd
from Constants import NASF_COLUMNS, GENERAL_COLUMNS, FILTER_VALUES


''' call using this syntax in terminal:
    [python executable] [path of sanitize_data.py] \
        [path of desired CSV to sanitize] [year]\
            [path of desired location and name of CSV]
    ex:./.env/python.exe ./src/sanitize_data.py \
        ./raw_data/facilities_2019_imputed.csv ./data/2019_sanitized.csv 2019
'''


def _parse_years(years):
    if isinstance(years, list):
        years = [int(year) for year in years]
        return years.sort()
    elif isinstance(years, str):
        return list(
            range(
                int(years.split(':')[0]),
                int(years.split(':')[-1]) + 1, 2))
    elif isinstance(years, int):
        return list(years)
    else:
        return 'Invalid YEAR value! Program will crash shortly.'


def _deparse_years(years_list):
    if isinstance(years_list, list):
        if len(years_list) > 1:
            years = str(min(years_list)) + '-' + str(max(years_list))
        else:
            years = str(years_list[0])
        return years
    else:
        return 'Invalid YEAR values! Program will crash shortly.'


def main():
    '''
    Handles main chunk of data sanitization, including initialization and
    path handling. Returns sanitized file. Currently uses hardcoded settings,
    however it would be nice to at some point revise it for
    argument-set instead. Pulls column names on a year-by-year basis
    from Constants.py
    '''
    # Basic argument handling and reporting back to user for debug purposes.
    origin_path, location, years_str = sys.argv[1:]
    # origin_path = abspath(origin_path)
    # location = abspath(location)
    print('Data File Directory:', origin_path)
    print('Location Directory: ', location)
    years = _parse_years(years_str)
    years_str = _deparse_years(years)
    print('Year(s): ' + years_str)
    data = dict()
    for year in years:
        # Reads data from CSV,
        # and then retrieves and aggregates into single list.
        data[year] = pd.read_csv(
            str(origin_path + 'facilities_' + str(year) + '.csv'),
            encoding='ISO-8859-1')
        valid_columns = [GENERAL_COLUMNS[year], NASF_COLUMNS[year]]
        valid_columns.extend(FILTER_VALUES[year].keys())
        # Iterates through keys of
        # FILTER_VALUES and adds all values to
        # list of valid_columns.
        valid_columns.extend(map(lambda x: FILTER_VALUES[year][x][1:],
                             FILTER_VALUES[year].keys()))
        # Since FILTER_VALUES is a dictionary of
        # list-of-lists with years as keys, once the
        # values (list-of-lists) have been added they must then be
        # unpacked to create a single list of Strings.
        # More info in Constants.py.
        valid_columns = [item for sublist in valid_columns for item in sublist]
        # Now that a list of all columns we want to keep has been assembled,
        # we can finally cut the dataset down to only those columns.
        data[year] = data[year].filter(items=valid_columns)
        # Filters only for values which have responses. Frankly I'm not sure
        # why they'd include non-Y answers in the dataset.
        data[year] = data[year][data[year]['SUBMISSION_FLAG'] == 'Y'].drop(
            labels='SUBMISSION_FLAG', axis=1)
        data[year] = data[year].replace('S', 0)
    Path(str(location + years_str + 'sanitized.csv')
         ).parent.mkdir(parents=True, exist_ok=True)
    data = pd.concat(data.values())
    data.to_csv(str(location + years_str + '_sanitized.csv'))
    print('Export Successful! Path: ', Path(
        str(location + years_str + 'sanitized.csv')))


if __name__ == '__main__':
    main()
