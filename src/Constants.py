# The goal is to make the data easier to standarize by having each set of
# collumns available under the 'category' and year the set applies to.

NASF_SUBJECT_LIST = {2007: ['AGR', 'BIO', 'COS', 'ENG', 'GEO', 'HLTH',
                            'MATH', 'NR', 'PHY1', 'PHY2', 'PSY', 'SOC', 'OTH',
                            'CLIN_TRIAL', 'MED'],
                     2011: ['AGR', 'BIO', 'COS', 'ENG', 'GEO', 'HLTH',
                            'MATH', 'PHY1', 'PHY2', 'PSY', 'SOC', 'OTH',
                            'CLIN_TRIAL', 'MED'],
                     2015: ['AG', 'BIO', 'COS', 'ENG',
                            'HLTH', 'MATH', 'NR', 'GEO', 'PHY', 'PSY', 'SOC',
                            'OTH', 'CLIN_TRIAL', 'MED']
                     }
NASF_PREFIXES = {2017: 'NASF_', 2015: 'Q2_', 2007: 'P1Q2'}


def get_NASF(year):
    prefix = NASF_PREFIXES[max(
        [x for x in NASF_PREFIXES.keys() if x <= year])]
    subjects = NASF_SUBJECT_LIST[max(
        [x for x in NASF_SUBJECT_LIST.keys() if x <= year])]
    return [prefix + x for x in subjects]


RR_SUBJECT_LIST = {2015: ['AG', 'BIO', 'COS', 'ENG',
                          'HLTH', 'MATH', 'NR', 'GEO', 'PHY', 'PSY', 'SOC',
                          'OTH', 'CLIN_TRIAL', 'MED'],
                   2011: ['AGR', 'BIO', 'COS', 'ENG', 'HLTH', 'MATH', 'PHY1',
                   'PHY2', 'PSY', 'SOC', 'OTH']
                   }

# annoyingly P1Q8 is the equivalent of RR_MED,
# so I'll have to add a special case in the translation function

RR_PREFIXES = {2017: 'RR_', 2015: 'Q7', 2011: 'P1Q7', 2007: 'P1Q9'}

# General but neccessary collumns.
# Usually has to do with the institution itself.
GENERAL_COLUMNS = {2019: [
    'YEAR', 'INST_ID', 'INST_NAME', 'SUBMISSION_FLAG',
    'INST_TYPE', 'INST_STATE', 'TOC_CODE', 'EXP_TOT_2018'], 2017: [
    'YEAR', 'INST_ID', 'INST_NAME', 'SUBMISSION_FLAG',
    'INST_TYPE', 'INST_STATE', 'TOC_CODE', 'EXP_TOT_2016'], 2015: [
    'YEAR', 'INST_ID', 'INST_NAME', 'SUBMISSION_FLAG',
    'INST_TYPE', 'INST_STATE', 'TOC_CODE', 'EXP_TOT_2014'], 2013: [
    'YEAR', 'INST_ID', 'INST_NAME', 'SUBMISSION_FLAG',
    'INST_TYPE', 'INST_STATE', 'TOC_CODE', 'EXP_TOT_2012'], 2011: [
    'YEAR', 'INST_ID', 'INST_NAME', 'SUBMISSION_FLAG',
    'INST_TYPE', 'INST_STATE', 'TOC_CODE', 'EXP_TOT_2010'], 2009: [
    'YEAR', 'INST_ID', 'INST_NAME', 'submission_flag', 'inst_type',
    'inst_state', 'toc_code', 'exp_tot_2008'], 2007: [
    'YEAR', 'INST_ID', 'INST_NAME', 'submission_flag', 'inst_type',
    'inst_state', 'toc_code', 'exp_tot_2006']
}


def get_general(year):
    return GENERAL_COLUMNS[max([x for x in GENERAL_COLUMNS.keys()
                                if x <= year])]


# This was originally going to be for the insertion of NaN into the dataset
# per row, but that ended up not being neccessary. Currently the only used
# key is 'SUBMISSION_FLAG', to filter for respondents, and the other entries
# are just used for pulling the valid column names.
# Strucuture is FILTER_VALUES[year][column_name], which returns a list of lists
# in which the first value is the "positive" or "goal" value, and the rest
# is the columns that should be made NaN if the key value is not
# FILTER_VALUES[year][column_name][0]
FILTER_VALUES = {
    2019:
    {'SUBMISSION_FLAG': ['Y', None],
     # 'RRBOX' onward is not needed, I'm just
     # keeping it in here in case it comes in useful later.
     'RRBOX':
     ['1', 'RR_AG', 'RR_BIO', 'RR_COS', 'RR_ENG', 'RR_GEO', 'RR_HLTH',
      'RR_MATH', 'RR_NR', 'RR_PHY', 'RR_PSY', 'RR_SOC', 'RR_OTH',
      'RR_TFUND', 'RR_CLIN_TRIAL', 'RR_MED'],
     'NCBOX': ['1', 'NC_FED', 'NC_STA', 'NC_INST', 'NC_TFUND'],
     'PNCBOX':
     ['1', 'PNC_AG_1', 'PNC_BIO_1', 'PNC_COS_1', 'PNC_ENG_1', 'PNC_GEO_1',
        'PNC_HLTH_1', 'PNC_MATH_1', 'PNC_NR_1', 'PNC_PHY_1', 'PNC_PSY_1',
        'PNC_SOC_1', 'PNC_OTH_1'
        'PNC_AG_2', 'PNC_BIO_2', 'PNC_COS_2', 'PNC_ENG_2', 'PNC_GEO_2',
        'PNC_HLTH_2', 'PNC_MATH_2', 'PNC_NR_2', 'PNC_PHY_2', 'PNC_PSY_2',
        'PNC_SOC_2', 'PNC_OTH_2'],
     'PRRBOX':
     ['1', 'PRR_AG', 'PRR_BIO', 'PRR_COS', 'PRR_ENG', 'PRR_GEO',
      'PRR_HLTH', 'PRR_MATH', 'PRR_NR', 'PRR_PHY', 'PRR_PSY', 'PRR_SOC',
      'PRR_OTH']
     }, 2017:
    {'SUBMISSION_FLAG': ['Y', None],
     # 'RRBOX' onward is not needed, I'm just
     # keeping it in here in case it comes in useful later.
     'RRBOX':
     ['1', 'RR_AG', 'RR_BIO', 'RR_COS', 'RR_ENG', 'RR_GEO', 'RR_HLTH',
      'RR_MATH', 'RR_NR', 'RR_PHY', 'RR_PSY', 'RR_SOC', 'RR_OTH',
      'RR_TFUND', 'RR_CLIN_TRIAL', 'RR_MED'],
     'NCBOX': ['1', 'NC_FED', 'NC_STA', 'NC_INST', 'NC_TFUND'],
     'PNCBOX':
     ['1', 'PNC_AG_1', 'PNC_BIO_1', 'PNC_COS_1', 'PNC_ENG_1', 'PNC_GEO_1',
        'PNC_HLTH_1', 'PNC_MATH_1', 'PNC_NR_1', 'PNC_PHY_1', 'PNC_PSY_1',
        'PNC_SOC_1', 'PNC_OTH_1'
        'PNC_AG_2', 'PNC_BIO_2', 'PNC_COS_2', 'PNC_ENG_2', 'PNC_GEO_2',
        'PNC_HLTH_2', 'PNC_MATH_2', 'PNC_NR_2', 'PNC_PHY_2', 'PNC_PSY_2',
        'PNC_SOC_2', 'PNC_OTH_2'],
     'PRRBOX':
     ['1', 'PRR_AG', 'PRR_BIO', 'PRR_COS', 'PRR_ENG', 'PRR_GEO',
      'PRR_HLTH', 'PRR_MATH', 'PRR_NR', 'PRR_PHY', 'PRR_PSY', 'PRR_SOC',
      'PRR_OTH']
     }, 2015:
    {'SUBMISSION_FLAG': ['Y', None],
     # 'RRBOX' onward is not needed, I'm just
     # keeping it in here in case it comes in useful later.
     'RRBOX':
     ['1', 'RR_AG', 'RR_BIO', 'RR_COS', 'RR_ENG', 'RR_GEO', 'RR_HLTH',
      'RR_MATH', 'RR_NR', 'RR_PHY', 'RR_PSY', 'RR_SOC', 'RR_OTH',
      'RR_TFUND', 'RR_CLIN_TRIAL', 'RR_MED'],
     'NCBOX': ['1', 'NC_FED', 'NC_STA', 'NC_INST', 'NC_TFUND'],
     'PNCBOX':
     ['1', 'PNC_AG_1', 'PNC_BIO_1', 'PNC_COS_1', 'PNC_ENG_1', 'PNC_GEO_1',
        'PNC_HLTH_1', 'PNC_MATH_1', 'PNC_NR_1', 'PNC_PHY_1', 'PNC_PSY_1',
        'PNC_SOC_1', 'PNC_OTH_1'
        'PNC_AG_2', 'PNC_BIO_2', 'PNC_COS_2', 'PNC_ENG_2', 'PNC_GEO_2',
        'PNC_HLTH_2', 'PNC_MATH_2', 'PNC_NR_2', 'PNC_PHY_2', 'PNC_PSY_2',
        'PNC_SOC_2', 'PNC_OTH_2'],
     'PRRBOX':
     ['1', 'PRR_AG', 'PRR_BIO', 'PRR_COS', 'PRR_ENG', 'PRR_GEO',
      'PRR_HLTH', 'PRR_MATH', 'PRR_NR', 'PRR_PHY', 'PRR_PSY', 'PRR_SOC',
      'PRR_OTH']
     },
}
