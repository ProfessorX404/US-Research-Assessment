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
    assert_equals({{'AG': 1291747.0, 'BIO': 1362821.0, 'COS': 138242.0,
                    'ENG': 1297715.0, 'GEO': 356720.0, 'HLTH': 1120561.0,
                    'MATH': 50010.0, 'NR': 0.0, 'PHY':1174583.0, 'PSY': 137168.0,
                    'SOC': 250954.0, 'OTH': 169063.0, 'CLIN_TRIAL': 0.0,
                    'MED': 1058810.0}, D2)
                   '''
    #print(D1)
    #print(D2)

    '''
    D3, D4 = data_analysis.subject_focus(d2019)
    assert_equals({'AG': 9, 'BIO': 21, 'COS': 19, 'ENG': 19, 'GEO': 14,
                   'HLTH': 17, 'MATH':16, 'NR':9, 'PHY':18, 'PSY':16, 'SOC': 16,
                   'OTH':3, 'CLIN_TRIAL':6, 'MED':5},
                   D3)
    #
    assert_equals({{'AG': 867350.0, 'BIO': 1872855.0, 'COS': 175036.0,
                    'ENG': 1568029.0, 'GEO': 425916.0, 'HLTH': 1003143.0,
                    'MATH': 62232.0, 'NR': 121484.0, 'PHY':1274448.0, 'PSY': 180386.0,
                    'SOC': 213774.0, 'OTH': 122865.0, 'CLIN_TRIAL': 83563.0,
                    'MED': 1141052.0}, D4)
                   '''
    #print(D3)
    #print(D4)
    print('not done!')


def test_calc_amt_growth():
    '''
    Tests the calc_amt_growth function from data_analysis.py
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
