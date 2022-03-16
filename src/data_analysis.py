'''
Natalie Dean, Xavier Beech
CSE163
Set of methods for the analysis of sanitized data from
the National Science Foundation's Survey of Science and Engineering Research.
More information on specific functions can be found in function headers.
'''
from pathlib import Path
from os.path import abspath
import pandas as pd
import geopandas as gpd
from Constants import abbrev_to_us_state
import matplotlib.pyplot as plt
import matplotlib as mpl
from collections import defaultdict

'''
call using path to the goal file
ie   ex:./.env/python.exe ./src/data_analysis.py \
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
# a new dataframe together) <-second might work better
# find a source of geodata and apply it to the dataset
# apply geopandas to the set to plot by location
# geodata obtained from:
# https://github.com/kjhealy/us-county/tree/master/data/geojson

# inelegant solution but just need to get code up and running
# can add argument intake for this instead at some point
path = './data/2007-2019_sanitized.csv'
geopath = './data/state_geodata.json'
pics_dir = './plots/'
DROP_STATES = ['Alaska', 'Hawaii',
               'Puerto Rico', 'Guam', 'U.S. Virgin Islands']
col_names = ['AG', 'BIO', 'COS', 'ENG', 'GEO', 'HLTH', 'MATH', 'NR', 'PHY',
             'PSY', 'SOC', 'CLIN_TRIAL', 'MED']

# step 2: research subject focus
# group by research areas
# sum square footage of areas
# Plot or print list of areas with most institutions, and list of areas
# with most square footage in institutions
# do max() and min() of subjects and spit those out (print?)


def subject_focus(data, to_plot=False):
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

    if to_plot:
        _plot_focus(subj_counts, subj_nasf)
    return [subj_counts, subj_nasf]


def _plot_focus(counts, nasf, fname = None):
    '''
    Helper function for subject_focus. Plots the results of analyis from the
    function on two separate plots, one for the most represented subjects and
    one for  the least represented subjects. Takes in two dictionaries
    of the counts of occurances and the numbers of allocated square footage.
    '''
    # sorts compiled data from largest to smallest
    counts = dict(sorted(counts.items(),
                         key=lambda item: item[1], reverse=True))
    nasf = dict(sorted(nasf.items(),
                       key=lambda item: item[1], reverse=True))

    # turns results into lists for quick access
    s_count = list(counts.values())
    s_count_key = list(counts.keys())
    s_nasf = list(nasf.values())
    s_nasf_key = list(nasf.keys())

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
    if fname is None:
        fig.savefig(pics_dir + "high_subjects.png")
    else:
        fig.savefig(pics_dir + fname + "_high.png")

    # plot top half of data
    ax4.bar(s_count_key[7:14], s_count[7:14],
            width=1, edgecolor="white", linewidth=0.7)
    ax4.set_ylabel("Number of institutions")
    ax5.bar(s_nasf_key[7:14], s_nasf[7:14],
            width=1, edgecolor="white", linewidth=0.7)
    ax5.set_ylabel("Total square footage")
    fig2.suptitle("Lower Half of Represented Subjects")
    if fname is None:
        fig2.savefig(pics_dir + "low_subjects.png")
    else:
        fig2.savefig(pics_dir + fname + "_low.png")

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
    NC_LIST = ['NC_FED', 'NC_STA', 'NC_INST']
    n = 5
    cols = [str('RR_' + name) for name in col_names
            if name not in RR_EXCEPT_THESE]
    # warning here; deprecated dropping of nuisance columns
    data['RR_SUM'] = data[cols].sum(axis=1)
    data['NC_SUM'] = data[NC_LIST].sum(axis=1)
    data['GROWTH_SUM'] = data[['RR_SUM', 'NC_SUM']].sum(axis=1)
    data['MAX_FUND'] = data[NC_LIST].apply(
        pd.to_numeric, errors='coerce').idxmax(
        axis=1, skipna=True)
    data['MIN_FUND'] = data[NC_LIST].apply(
        pd.to_numeric, errors='coerce').idxmin(axis=1)
    data['SINGLE_FUND'] = data['MAX_FUND'] == data['MIN_FUND']
    for n in range(1, n + 1):
        data[str(n) + '_FUNDED'] =\
            data[cols].columns[data[cols].apply(
                pd.to_numeric, errors='coerce').values.argsort(1)[:, -n]]
    data = data.rename(index=data['INST_STATE'])
    return data


# create a bar graph with largest changes in numbers of institutions by state?
# plot of subject areas' number of occurances over time
# and/or square footage amounts over time
def multi_plot(data):
    '''
    Plots the components of the above function involving analysis over multiple
    years of data. Takes in a dataframe including all years of data from
    2007-2019. Specifically, it aggregates and plots data relating to the
    number of institutions pursuing research in a given field, and the
    square footage dedicated to that research nationwide.
    '''
    years = list(range(min(data['YEAR']), max(data['YEAR'] + 1), 2))

    # Collect our counts and NASFs by area by year, then convert into a dict.
    # of lists of these for plotting
    cts = dict()
    nasf = dict()
    data.drop(['NASF_OTH', 'RR_OTH'], axis=1)
    for year in years:
        cts[year], nasf[year] = subject_focus(data[data['YEAR'] == year])
    all_cts = defaultdict(list)
    all_nasf = defaultdict(list)
    for name in col_names:
        for year in years:
            all_cts[name].append(cts[year][name])
            all_nasf[name].append(nasf[year][name])

    s_count = list(all_cts.values())
    s_nasf = list(all_nasf.values())
    fig, [ax, ax2] = plt.subplots(2)
    i = 0
    for name in col_names:
        ax.plot(years, s_count[i], label=name)
        ax2.plot(years, s_nasf[i], label=name)
        i += 1
    ax.set_xlabel('Fiscal Year')
    ax2.set_xlabel('Fiscal Year')

    ax.set_ylabel('Number of Institutions')
    ax2.set_ylabel('Amount of Square Feet')

    ax.set_title('Institutions with Dedicated Space for Subject Research')
    ax2.set_title(
        'Dedicated Space (in sq. ft.) for Subject Research Nationally', y=1.1)

    lines_labels = [ax.get_legend_handles_labels()]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    fig.legend(lines, labels, bbox_to_anchor=(
        .85, -.05), ncol=len(lines) // 3)
    fig.subplots_adjust(hspace=1)
    fig.savefig(pics_dir + "subj_trends.png", bbox_inches="tight")


def _plot_map(
        data, geo, column, func=None, ax=None, log_norm: bool = False,
        legend='True', legend_kwds=None, groupby='INST_STATE',
        geo_merge='NAME', how='right', dropna: bool = True,
        categorical: bool = False, scale=1):
    '''
    A multipurpose helper function that plots or maps a given dataset based on
    the indicated inputs. Data is the dataframe, geo is incoming geodata, func
    may be either 'sum' or 'count' (indicating what type of groupby to use)
    and if func is not defined it is instead assumed categorical analysis will
    be performed. An axis may also be passed in for multiple plots on the
    same axis, and parameters may be used to define presence or absence of
    a legend, legend keywords, what to group by and merge, which side to merge
    by, and whether to drop NaN values.
    Returns the figure on which the plot has been assembled.
    '''
    if ax is None:
        plt.clf()
        ax = plt.subplots(1)[1]
    # group data by state (add func cases as needed)
    if func == 'sum':
        data[column] = pd.to_numeric(data[column], errors='coerce')
        data = data.groupby(by=groupby).sum()
        # print('after', data['EXP_TOT'])
    elif func == 'count':
        data[column] = pd.to_numeric(data[column], errors='coerce')
        data = data.groupby(by=groupby).count()
    elif func is None:
        categorical = True
    else:
        print('Invalid func: ', str(func))
        return None
    # merges shapefile with our counts data
    full_snames = {s: abbrev_to_us_state[s] for s in data.index}
    data = data.rename(index=full_snames)
    groupby = data.index
    geo.plot(ax=ax, color='#EEEEEE')  # plots all states before merge
    geo = geo.merge(data, left_on=geo_merge, right_on=groupby,
                    how=how)
    # filters out dropped vals
    if dropna:
        geo = geo.dropna(axis=0, how='any')
    if scale != 1:
        data[column] = data[column] * scale
    if log_norm:
        geo.plot(ax=ax, column=column, legend=legend, legend_kwds=legend_kwds,
                 norm=mpl.colors.LogNorm(
                     vmin=geo[column].min() + 1,
                     vmax=geo[column].max()))
    elif categorical:
        geo.plot(ax=ax, column=column, legend=legend,
                 categorical=categorical, legend_kwds=legend_kwds)
    else:
        geo.plot(ax=ax, column=column, legend=legend, legend_kwds=legend_kwds)
    return ax


def _save_fig(title, dir=None, filename=None, abs=None):
    '''
    Saves the resulting plot from data analysis to a new file. Values passed in
    are the figure title, the directory name, the file name, and an absolute
    path. If the absolute path is not passed in, one will be created.
    '''
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
    combined = combined[~combined['NAME'].isin(DROP_STATES)]

    # runs our functions

    # Extracts specific datasets for years, as needed
    d2019 = data.copy(deep=True)  # copies dataframe so Pandas doesn't get mad
    d2019 = d2019[d2019['YEAR'] == 2019]  # filters for only target year
    # Maps amount of research institutions by state. for 2019
    _plot_map(
        d2019, combined, func='count', column='Unnamed: 0')
    _save_fig('Number of Institutions by State',
              dir=pics_dir, filename='state_insts.png')
    # Plots top and bottom 7 areas by number of institutions and sq. footage
    subject_focus(d2019, True)
    # Maps investment in growth by state for 2019
    growth_data = calculate_amount_of_growth(d2019)
    # Plots investment in growth by state for 2019
    _plot_map(
        growth_data, combined, func='sum', column='EXP_TOT',
        log_norm=True, dropna=False)
    _save_fig('R&D Expenditures in 2018, by State ($)',
              dir=pics_dir, filename='state_growth.png')
    # Plots primary funding source for growth in each state
    _plot_map(
        growth_data, combined, column='MAX_FUND', categorical=True,
        legend_kwds={'loc': 'lower right', 'fontsize': 'small'}, dropna=False)
    _save_fig('Primary Funding Source by State',
              dir=pics_dir, filename='state_funding.png')
    multi_plot(data)
    print('Done!')


if __name__ == '__main__':
    main()
