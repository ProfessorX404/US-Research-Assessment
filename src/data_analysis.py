from pathlib import Path
import sys
from os.path import abspath
import pandas as pd
#import geopandas as gpd
#import matplotlob.pyplot as plt

'''
call using path to the goal file
ie   ex:./.env/python.exe ./src/sanitize_data.py \
        ./data/2019_sanitized.csv
        --there's probably a better way to do this for multiple files--
'''

#Goals for this file: carry out bulk of data analysis
#Might need to split it up eventually but it should be pretty straightforward
#once the infrastructure is down

#step 1: regional analysis
#import data file
#convert to dataframe
#group data by state
#sort by year (not our problem yet; would probably need to be handled outside
#of this function with some sort of return infrastructure/combining into
#a new dataframe together) <-second might work better
#find a source of geodata and apply it to the dataset
#apply geopandas to the set to plot by location
#implement later: potentially compare over time and plot largest changes
def regional_analysis(data):
    '''
    Outputs analysis of research institutions by location, given a dataset in
    the form of a dataframe. Creates a geopandas visualization of occurances of
    schools by state.
    '''
    #group data by state (count all occurances of each)
    counts = data.groupby(by='INST_STATE').count()
    #print(counts.head()) #for testing
    #apply geodata:
    #shapefile from
    #https://hub.arcgis.com/datasets/CMHS::states-shapefile/explore?location=28.177808%2C-105.995557%2C3.79
    #intent is to test this file once I have geopandas up and running

#step 2: research subject focus
#group by research areas
#sum square footage of areas
#Plot or print list of areas with most institutions, and list of areas
#with most square footage in institutions
#do max() and min() of subjects and spit those out (print?)
def subject_focus(data):
    '''
    Outputs informatin on research subjects and the broadness of their
    representation in institutions across the country, given the dataset
    for a single year. Examines which research subjects are represented
    among the most institutions, and which subjects are given the most
    square footage among institutions, and compares the two.
    '''
    col_names = ['AG', 'BIO', 'COS', 'ENG', 'GEO', 'HLTH', 'MATH', 'NR', 'PHY',
                 'PSY', 'SOC', 'OTH', 'CLIN_TRIAL', 'MED']
    subj_counts = dict()
    subj_nasf = dict()
    # calculates the number of schools represented in each areas
    for name in col_names:
        col = None
        col = str('NASF_' + name)
        # sorts out numerical data that is nonzero
        has_space = data[(data[col] != 0) & (data[col] != 'S')]
        # converts from string and sums space
        amt_space = pd.to_numeric(has_space[col]).sum()
        subj_counts[name] = len(has_space[col])
        subj_nasf[name] = amt_space

    # sorts compiled data from largest to smallest; easy to reorder if needed
    subj_counts = dict(sorted(subj_counts.items(),
                       key = lambda item: item[1], reverse=True))
    subj_nasf = dict(sorted(subj_nasf.items(),
                     key = lambda item: item[1], reverse=True))
    print(subj_counts)
    print(subj_nasf)
    # still need to plot all this!


#step 3: monetary support of instituions
#sum amounts of R/R and new construction per institution
#pair these sums with the listed sources of funding
#compare the sums of funding sources and occurances of funding sources (as in 2)
#stretch: look at correlation between institution type and funding source
#or state and funding source
def amount_of_growth(data):
    '''
    Outputs analysis of growth of research institutions, represented by the
    amounts of funding they receive for R/R and new construction. Sums the
    quantities of funding attained by institution and compares the sources
    of funding and their contribution.
    '''


def main():
    #my path, dropping in so I can call from atom
    path = './data/2019_sanitized.csv'

    #import data file, convert to dataframe- idk if this works
    dpath = sys.argv[1:]

    data = pd.read_csv(abspath(path), encoding='ISO-8859-1') #might work
    regional_analysis(data)
    subject_focus(data)

if __name__ == '__main__':
    main()
