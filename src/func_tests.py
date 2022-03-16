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
import geopandas as gpds

path_2007 = './data/2007_test.csv'
path_2019 = './data/2019_test.csv'


def test_school_locs():
    print('not done!')


def test_subject_focus():
    print('not done!')


def test_calc_amt_growth():
    print('not done!')


def test_multi_plot():
    print('not done!')


def main():
    d2007 = pd.read_csv(abspath(path_2007), encoding='ISO-8859-1')
    d2019 = pd.read_csv(abspath(path_2019), encoding='ISO-8859-1')
    print(d2007.head())
    print(d2019.head())


if __name__ == '__main__':
    main()
