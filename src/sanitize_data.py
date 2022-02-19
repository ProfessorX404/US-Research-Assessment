from pathlib import Path
import sys
from os.path import abspath
import pandas as pd
from Constants import NASF_COLUMNS, GENERAL_COLUMNS, FILTER_VALUES
import numpy as np


''' call using this syntax in terminal:
    [python executable] [path of sanitize_data.py] \
        [path of desired CSV to sanitize] [year]\
            [path of desired location and name of CSV]
    ex:./.env/python.exe ./src/sanitize_data.py \
        ./raw_data/facilities_2019_imputed.csv ./data/2019_sanitized.csv 2019
'''


def filter_df(df, filter_title, filter_val='1', valid_columns=None):
    if valid_columns is None:
        return df[df[filter_title] == filter_val]
    else:
        for collumn in valid_columns:
            print(filter_title + filter_val)
            print(df[filter_title])
            df.loc[df[filter_title] == filter_val, filter_title] = np.nan
        return df


def export_to_csv(df, file_path):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path)
    print('Export Successful!')


def get_list_from_LoL(list_of_lists):
    main_list = []
    for lists in list_of_lists:
        for lists in lists:
            if lists != []:
                main_list.append(lists)
    return main_list


def filter_columns(df, valid_columns):
    return df.filter(items=valid_columns)


def main():
    origin_path, location, year = sys.argv[1:]
    year = int(year)
    print('Data File Path:', abspath(origin_path))
    print('Location Path: ', abspath(location))
    print('Year: ', int(year))
    data = pd.read_csv(abspath(origin_path), encoding='ISO-8859-1')
    valid_columns = [GENERAL_COLUMNS[year], NASF_COLUMNS[year]]
    valid_columns.extend(map(lambda x: FILTER_VALUES[year][x][1:],
                             FILTER_VALUES[year].keys()))
    valid_columns = get_list_from_LoL(valid_columns)
    data = filter_columns(data, valid_columns)
    for val in FILTER_VALUES[year].keys():
        data = filter_df(
            data, val, FILTER_VALUES[year][val][0],
            FILTER_VALUES[year][val][1:])
    export_to_csv(data, location)


if __name__ == '__main__':
    main()
