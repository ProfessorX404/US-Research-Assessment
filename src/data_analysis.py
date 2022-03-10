'''
Natalie Dean, Xavier Beech
CSE163
Set of methods for the analysis of sanitized data from
the National Science Foundation's Survey of Science and Engineering Research.
More information on specific functions can be found in function headers.
'''
from pathlib import Path
# import sys
from os.path import abspath
import pandas as pd
import geopandas as gpd
from state_abbrev import abbrev_to_us_state
import matplotlib.pyplot as plt
import matplotlib as mpl
import Constants

'''
call using path to the goal file
ie   ex:./.env/python.exe ./src/sanitize_data.py \
        ./data/2019_sanitized.csv
        --there's probably a better way to do this for multiple files--
'''

# Goals for this file: carry out bulk of data analysis
# Might need to split it up eventually but it should be pretty straightforward
# once the infrastructure is down

#  step 1: regional analysis
#  import data file
# convert to dataframe
# group data by state
# sort by year (not our problem yet; would probably need to be handled outside
# of this function with some sort of return infrastructure/combining into
# a new dataframe together) <-second might work better
# find a source of geodata and apply it to the dataset
# apply geopandas to the set to plot by location
# implement later: potentially compare over time and plot largest changes
# geodata obtained from:
# https://github.com/kjhealy/us-county/tree/master/data/geojson

# inelegant solution but just need to get code up and running
# can add argument intake for this instead at some point
year = 2019
path = './data/2019_sanitized.csv'
geopath = './data/state_geodata.json'
pics_dir = './plots/'


# step 2: research subject focus
# group by research areas
# sum square footage of areas
# Plot or print list of areas with most institutions, and list of areas
# with most square footage in institutions
# do max() and min() of subjects and spit those out (print?)


col_names = ['AG', 'BIO', 'COS', 'ENG', 'GEO', 'HLTH', 'MATH', 'NR', 'PHY',
             'PSY', 'SOC', 'OTH', 'CLIN_TRIAL', 'MED']


def subject_focus(data):
    '''
    Outputs information on research subjects and the broadness of their
    representation in institutions across the country, given the dataset
    for a single year. Examines which research subjects are represented
    among the most institutions, and which subjects are given the most
    square footage among institutions, and compares the two.
    '''
    subj_counts = dict()
    subj_nasf = dict()
    # calculates the number of schools represented in each areas
    for name in col_names:
        col = None
        col = str('NASF_' + name)
        # sorts out numerical data that is nonzero
        has_space = data[(data[col] != 0)]
        # converts from string and sums space
        amt_space = pd.to_numeric(has_space[col]).sum()
        subj_counts[name] = len(has_space[col])
        subj_nasf[name] = amt_space

    # sorts compiled data from largest to smallest; easy to reorder if needed
    subj_counts = dict(sorted(subj_counts.items(),
                       key=lambda item: item[1], reverse=True))
    subj_nasf = dict(sorted(subj_nasf.items(),
                     key=lambda item: item[1], reverse=True))

    # turns results into lists for quick access
    s_count = list(subj_counts.values())
    s_count_key = list(subj_counts.keys())
    s_nasf = list(subj_nasf.values())
    s_nasf_key = list(subj_nasf.keys())

    fig, [ax2, ax3] = plt.subplots(2)
    fig2, [ax4, ax5] = plt.subplots(2)
    # plot top half of data
    ax2.bar(s_count_key[0:7], s_count[0:7],
            width=1, edgecolor="white", linewidth=0.7)
    ax2.set_ylabel("Number of institutions")
    ax3.bar(s_nasf_key[0:7], s_nasf[0:7],
            width=1, edgecolor="white", linewidth=0.7)
    ax3.set_ylabel("Total square footage")
    #  plt.title("Total Square Footage Per Subject")
    fig.suptitle("Upper Half of Represented Subjects")
    fig.savefig(pics_dir + "high_subjects.png")

    # plot top half of data
    ax4.bar(s_count_key[7:14], s_count[7:14],
            width=1, edgecolor="white", linewidth=0.7)
    ax4.set_ylabel("Number of institutions")
    ax5.bar(s_nasf_key[7:14], s_nasf[7:14],
            width=1, edgecolor="white", linewidth=0.7)
    ax5.set_ylabel("Total square footage")
    fig2.suptitle("Lower Half of Represented Subjects")
    fig2.savefig(pics_dir + "low_subjects.png")


# step 3: monetary support of instituions
# sum amounts of R/R and new construction per institution
# pair these sums with the listed sources of funding
# compare the sums of funding sources and
# occurances of funding sources (as in 2)
# stretch: look at correlation between institution type and funding source
# or state and funding source
def calculate_amount_of_growth(data):
    '''
    Outputs analysis of growth of research institutions, represented by the
    amounts of funding they receive for R/R and new construction. Sums the
    quantities of funding attained by institution and compares the sources
    of funding and their contribution. Returns new dataframe with associated
    columns, to facilitate easier transition to plotting.
    '''
    RR_EXCEPT_THESE = ['CLIN_TRIAL']
    NC_LIST = ['NC_FED', 'NC_STA', 'NC_INST', 'NC_TFUND']
    RETURN_LIST = Constants.GENERAL_COLUMNS[year]
    RETURN_LIST.extend([
        'RR_SUM', 'NC_SUM', 'GROWTH_SUM', 'MAX_FUND', 'MIN_FUND',
        'SINGLE_FUND'])
    n = 5
    # data['RR_SUM'] = numpy.np.zeros(data.shape[0] - 1, 1)
    cols = [str('RR_' + name) for name in col_names
            if name not in RR_EXCEPT_THESE]
    data['RR_SUM'] = data[cols].sum(axis=1)
    data['NC_SUM'] = data[NC_LIST].sum(axis=1)
    data['GROWTH_SUM'] = data[['RR_SUM', 'NC_SUM']].sum(axis=1)
    data['MAX_FUND'] = data[NC_LIST].idxmax(axis=1, skipna=True)
    data['MIN_FUND'] = data[NC_LIST].idxmin(axis=1)
    data['SINGLE_FUND'] = data['MAX_FUND'] == data['MIN_FUND']
    for n in range(1, n + 1):
        data[str(n) + '_FUNDED'] =\
            data[cols].columns[data[cols].values.argsort(1)[:, -n]]
        # RETURN_LIST.append(str(n) + '_FUNDED')
    RETURN_LIST.remove("SUBMISSION_FLAG")
    data = data.rename(index=data['INST_STATE'])
    return data[RETURN_LIST]


def plot_map(
        data, geo, column, func=None, ax=None, log_norm: bool = False,
        legend='True', groupby='INST_STATE', geo_merge='NAME', how='right',
        dropna: bool = True, categorical: bool = False):
    if ax is None:
        plt.clf()
        ax = plt.subplots(1)[1]
    # group data by state (add func cases as needed)
    if func == 'sum':
        data = data.groupby(by=groupby).sum()
    elif func == 'count':
        data = data.groupby(by=groupby).count()
    elif func is None:
        categorical = True
    else:
        print('Invalid func: ', str(func))
        return None
    # merges shapefile with our counts data
    full_snames = {s: abbrev_to_us_state[s] for s in data.index}
    data = data.rename(index=full_snames)
    groupby=data.index
    geo = geo.merge(data, left_on=geo_merge, right_on=groupby,
                    how=how)
    # filters out outlying territories that'll harm the map scale
    # filters out dropped vals
    if dropna:
        geo = geo.dropna(axis=0, how='any')
    # undecided if I want to log normalize the colors, the graph
    # is kind of hard to look at and isn't super readable.
    if log_norm:
        print('here1')
        geo.plot(ax=ax, column=column, legend=legend,
                 norm=mpl.colors.LogNorm(
                     vmin=geo[column].min() + 1,
                     vmax=geo[column].max()))
    elif categorical:
        # This is where I'm seeing the error about trying to plot the empty
        # dataframe. However I think the actual issue is up above at 179.
        # The only categorical data we're graphing currently is line 246,
        # about the largest funding source by state.
        print('here2')
        geo.to_csv(r'plzwork.csv')
        print(geo)
        geo.plot(ax=ax, column=column, legend=legend, categorical=categorical)
    else:
        print('here3')
        geo.plot(ax=ax, column=column, legend=legend)


def save_fig(title, dir=None, filename=None, abs=None):
    plt.title(title)
    if abs is None:
        Path(abspath(dir + filename)).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(abspath(dir + filename))
    else:
        Path(abs).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(abs)


def main():

    # import data file, convert to dataframe- idk if this works
    # dpath, gpath = sys.argv[1:] # going unused right now
    data = pd.read_csv(abspath(path), encoding='ISO-8859-1')

    # imports geodata and filters out outlying areas
    combined = gpd.read_file(abspath(geopath), encoding='utf-8')
    combined = combined[(combined['NAME'] != 'Alaska')
                        & (combined['NAME'] != 'Hawaii')
                        & (combined['NAME'] != 'Puerto Rico')]

    # runs our functions

    # Maps amount of research institutions by state.
    plot_map(
        data, combined, func='count', column='Unnamed: 0')
    save_fig('Number of Institutions by State',
             dir=pics_dir, filename='state_insts.png')
    # Plots top and bottom 7 areas by number of institutions and sq. footage.
    subject_focus(data)
    # Maps investment in growth by state.
    growth_data = calculate_amount_of_growth(data)
    # Plots investment in growth by state
    plot_map(growth_data, combined, func='sum',
             column='GROWTH_SUM', log_norm=True)
    save_fig('Growth in 2019, by State($)',
             dir=pics_dir, filename='state_growth.png')
    # Plots primary funding source for growth in each state
    plot_map(growth_data, combined, column='MAX_FUND',
             categorical=True)
    save_fig('Primary Funding Source by State',
             dir=pics_dir, filename='state_funding.png')


if __name__ == '__main__':
    main()
