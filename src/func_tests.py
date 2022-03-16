'''
Xavier Beech, Natalie Dean
CSE163
Tests the functions implemented in data_analysis.py. Uses two shortened
datasets and compares them to calculated values and intended graphs.
'''
import data_analysis
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


def test_subject_focus(d2007, d2019):
    '''
    Tests the subject_focus method from data_analysis.py
    '''
    # Tests 2007 dataset. Comparison values determined manually via Excel.
    D1, D2 = data_analysis.subject_focus(d2007)
    assert_equals(
        {'AG': 8, 'BIO': 20, 'COS': 18, 'ENG': 15, 'GEO': 13, 'HLTH': 14,
         'MATH': 16, 'NR': 0, 'PHY': 18, 'PSY': 16, 'SOC': 17,
         'CLIN_TRIAL': 0, 'MED': 5},
        D1)
    assert_equals({'AG': 1291747, 'BIO': 1362821, 'COS': 138242,
                   'ENG': 1297715, 'GEO': 356720, 'HLTH': 1120561,
                   'MATH': 50010, 'NR': 0, 'PHY': 1174583, 'PSY': 137168,
                   'SOC': 250954, 'CLIN_TRIAL': 0,
                   'MED': 1058810}, D2)

    # Tests 2019 dataset. Comparison values determined manually via Excel.
    D3, D4 = data_analysis.subject_focus(d2019)
    assert_equals(
        {'AG': 9, 'BIO': 21, 'COS': 19, 'ENG': 19, 'GEO': 14, 'HLTH': 17,
         'MATH': 16, 'NR': 9, 'PHY': 18, 'PSY': 16, 'SOC': 16,
         'CLIN_TRIAL': 6, 'MED': 5},
        D3)
    assert_equals({'AG': 867350, 'BIO': 1872855, 'COS': 175036,
                   'ENG': 1568029, 'GEO': 425916, 'HLTH': 1003143,
                   'MATH': 62232, 'NR': 121484, 'PHY': 1274448, 'PSY': 180386,
                   'SOC': 213774, 'CLIN_TRIAL': 83563,
                   'MED': 1141052}, D4)

    # Tests plotting of both datasets:
    # For 2007: Bio, cos/phy, soc highest num, Bio, engr, ag, highest NASF
    data_analysis._plot_focus(D1, D2, "2007_test")

    # For 2019: Bio, cos/eng, phy, hlth high num, bio, eng, phy high NASF
    data_analysis._plot_focus(D3, D4, "2019_test")


def test_calc_amt_growth(d2007, d2019, combined):
    '''
    Tests the calc_amt_growth function from data_analysis.py
    '''
    d07 = data_analysis.calculate_amount_of_growth(d2007)
    d19 = data_analysis.calculate_amount_of_growth(d2019)
    # plots for 2007; we expect the highest funding sources for states to be:
    # AL: state, AR: inst, AZ:state, CA:state
    # Expect AK < CA < AL < AZ
    data_analysis._plot_map(
        d07, combined, func='sum', column='EXP_TOT',  # ERROR HERE!!!!
        log_norm=True, dropna=False)
    data_analysis._save_fig('R&D Expenditures (Test 2007)',
                            dir=pics_dir, filename='growth_2007test.png')
    data_analysis._plot_map(
        d07, combined, column='MAX_FUND', categorical=True,
        legend_kwds={'loc': 'lower right', 'fontsize': 'small'}, dropna=False)
    data_analysis._save_fig('Primary Funding Source by State',
                            dir=pics_dir, filename='fund_2007test.png')
    # plots for 2019: we expect highest funding sources for states to be:
    # AL:Inst AZ:Inst CA:Fed AK: Fed
    # Expect AZ < CA < AK < AL
    data_analysis._plot_map(
        d19, combined, func='sum', column='EXP_TOT',
        log_norm=True, dropna=False)
    data_analysis._save_fig('R&D Expenditures (Test 2007)',
                            dir=pics_dir, filename='growth_2019test.png')
    data_analysis._plot_map(
        d19, combined, column='MAX_FUND', categorical=True,
        legend_kwds={'loc': 'lower right', 'fontsize': 'small'}, dropna=False)
    data_analysis._save_fig('Primary Funding Source by State',
                            dir=pics_dir, filename='fund_2019test.png')


def test_multi_plot(d2007, d2019):
    '''
    Tests the multi_plot function from data_analysis.py
    '''
    dcombined = pd.concat([d2007, d2019], ignore_index=True)
    data_analysis.multi_plot(dcombined, '2007_19_test')
    print('not done!')


def main():
    d2007 = pd.read_csv(abspath(path_2007), encoding='ISO-8859-1')
    d2019 = pd.read_csv(abspath(path_2019), encoding='ISO-8859-1')

    combined = gpd.read_file(abspath(geopath), encoding='utf-8')
    combined = combined[~combined['NAME'].isin(DROP_STATES)]

    # test Counts
    test_school_locs(d2007, d2019, combined)

    # test focus
    test_subject_focus(d2007, d2019)

    # test funding
    test_calc_amt_growth(d2007, d2019, combined)

    # test multi_plot
    test_multi_plot(d2007, d2019)


if __name__ == '__main__':
    main()
