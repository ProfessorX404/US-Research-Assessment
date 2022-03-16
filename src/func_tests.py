'''
Xavier Beech, Natalie Dean
CSE163
Tests the functions implemented in data_analysis.py. Uses two shortened
datasets and compares them to calculated values and intended graphs.
'''
import data_analysis
from pathlib import Path
from os.path import abspath
import pandas as pd
import geopandas as gpd
from cse163_utils import assert_equals

path_2007 = './data/2007_test.csv'
path_2019 = './data/2019_test.csv'
geopath = './data/state_geodata.json'
DROP_STATES = ['Alaska', 'Hawaii', 'Puerto Rico']
pics_dir = './plots/'

def test_school_locs(d2007, d2019, combined):
    '''
    Tests functionality of counting school locations per state
    by plotting them with two different years' datasets and comparing
    '''
    # test 1: should have 7 AL, 5 CA, 3 AZ, 6 AR
    data_analysis._plot_map(d2007, combined, func='count',
                            column='Unnamed: 0')
    data_analysis._save_fig('Counts by State (TEST, 2019)',
                            dir=pics_dir, filename='test_2007cts.png')

    # test 2: should have 5 CA, 3 AZ, 7 AL, 6 AR (aka should be identical)
    data_analysis._plot_map(d2019, combined, func='count',
                            column='Unnamed: 0')
    data_analysis._save_fig('Counts by State (TEST, 2019)',
                            dir=pics_dir, filename='test_2019cts.png')


def test_subject_focus(d2007, d2019, combined):
    '''
    Tests the subject_focus method from data_analysis.py
    '''
    # 2007: AG: 8, BIO: 20, COS: 18, ENG: 15, HLTH: 14, MATH: 16, GEO: 13,
    # PHY: 18, PSY: 16, SOC: 17, NA/CLIN_TRIAL: 0 (not counted this year)
    D1, D2 = data_analysis.subject_focus(d2007)
    '''
    assert_equals({'AG': 8, 'BIO': 20, 'COS': 18, 'ENG': 15, 'GEO': 13,
                   'HLTH': 14, 'MATH':16, 'NR':0, 'PHY':18, 'PSY':16, 'SOC': 17,
                   'OTH':5, 'CLIN_TRIAL':0, 'MED':5},
                   D1)
    #
    assert
                   '''
    print(D1)
    print(D2)


    print('not done!')


def test_calc_amt_growth():
    '''

    '''
    print('not done!')


def test_multi_plot():
    '''

    '''
    prit('not done!')

def main():
    d2007 = pd.read_csv(abspath(path_2007), encoding='ISO-8859-1')
    d2019 = pd.read_csv(abspath(path_2019), encoding='ISO-8859-1')
    print(d2007.head())
    print(d2019.head())
    combined = gpd.read_file(abspath(geopath), encoding='utf-8')
    combined = combined[~combined['NAME'].isin(DROP_STATES)]

    # test Counts
    test_school_locs(d2007, d2019, combined)

    # test focus
    test_subject_focus(d2007, d2019, combined)


if __name__ == '__main__':
    main()
