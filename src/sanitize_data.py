'''
Xavier Beech, Natalie Dean
CSE163
Sanitizes the National Science Foundation's Survey of
Science and Engineering Research Facilities.
Dataset information can be found in
./raw_data/2019-faciliities-puf-user-guide.pdf
'''
from pathlib import Path
import sys
import pandas as pd
from Constants import get_column


''' call using this syntax in terminal:
    [python executable] [path of sanitize_data.py] \
        [raw_data path] \
            [data directory path] [year(s)*]
    ex:./.env/python.exe ./src/sanitize_data.py \
        ./raw_data/ ./data/ '2015:2019'
    *possible year formats:
        -Single year: 2019, '2019'
        -Multiple years: [2015, 2017, 2019], ['2015', '2017', '2019'],
                         '2015:2019'
'''


def _parse_years(years):
    '''
    Simple helper method to turn variety of possible String inputs
    from arguments into list of years for the main method to churn through.
    '''
    if isinstance(years, str):
        if years[0] == '[':
            print(years)
            years = years[1:len(years)-1]
            print(years)
            years = years.split(',')
            print(years)
            years = [int(year) for year in years]
            return years.sort()
        return list(
            range(
                int(years.split(':')[0]),
                int(years.split(':')[-1]) + 1, 2))
    elif isinstance(years, int):
        return list(years)
    else:
        return 'Invalid YEAR value! Program will crash shortly.'


def _deparse_years(years_list):
    '''
    Simple helper method to take list of years and turn it back into
    a string for file-naming purposes.
    '''
    if isinstance(years_list, list):
        if len(years_list) > 1:
            years = str(min(years_list)) + '-' + str(max(years_list))
        else:
            years = str(years_list[0])
        return years
    else:
        return 'Invalid YEAR list! Program will crash shortly.'


def main():
    '''
    Handles main chunk of data sanitization, including initialization and
    path handling. Returns sanitized file. Currently uses hardcoded settings,
    however it would be nice to at some point to revise it for
    argument-set instead. Pulls column names on a year-by-year basis
    from Constants.py
    '''
    # Basic argument handling and read-back.
    origin_path, location = sys.argv[1:3]
    years_str = sys.argv[3:]
    print('Data File Directory:', origin_path)
    print('Location Directory: ', location)
    years = [2007]  # _parse_years(years_str)
    years_str = _deparse_years(years)
    print('Year(s): ' + years_str)
    # data is the dictionary that will hold the DataFrames for each year.
    data = dict()
    # storage variable for tracking continuous indexing of each year
    index_start = 0
    for year in years:
        # Reads data from CSV,
        # and then retrieves and aggregates into single list.
        data[year] = pd.read_csv(
            str(origin_path + 'facilities_' + str(year) + '.csv'),
            encoding='ISO-8859-1')
        valid_columns = get_column(year, -1)
        # Cuts dataset down to only columns we need to keep.
        data[year] = data[year].filter(items=valid_columns)
        # Filters only for values which have responses. Frankly I'm not sure
        # why they'd include non-Y answers in the dataset.
        data[year] = data[year][
            data[year][get_column(year, 'SUBMISSION_FLAG')] == 'Y'].drop(
            labels=get_column(year, 'SUBMISSION_FLAG'), axis=1)
        # Some datasets for some reason have 'S' instead of Nan or 0
        data[year] = data[year].replace(['S', 'M'], 0)
        # Renames all years of columns to 2019 standard
        # (or technically the last available year)
        # Also worth notiing is the format that the
        # Constants dictionary is in is backwards
        # for readabilities sake, so it flips the key-value
        # order to be parsed by rename().
        data[year] = data[year].rename(columns=dict(
            (v, k) for k, v in get_column(year).items()))

        data[year][[k for k, v in get_column(year).items() if v is None]] = 0
        # sets each year to have indexes following the previous year.
        new_index = {x: x+index_start for x in data[year].index}
        data[year] = data[year].rename(
            index=new_index)
        index_start += list(new_index.keys())[-1] + 1
    Path(str(location + years_str + '_sanitized.csv')
         ).parent.mkdir(parents=True, exist_ok=True)
    # merges all years into single continugous DataFrame.
    data = pd.concat(data.values())
    data = data.replace(r'^\s*$', 0, regex=True)
    # exports mega-DataFrame to csv.
    data.to_csv(str(location + years_str + '_sanitized.csv'))
    print('Export Successful! Path: ', Path(
        str(location + years_str + '_sanitized.csv')))


if __name__ == '__main__':
    main()
