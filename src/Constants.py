NASF_COLUMNS = {2019: [
    'NASF_AG', 'NASF_BIO', 'NASF_COS', 'NASF_ENG', 'NASF_GEO', 'NASF_HLTH',
    'NASF_MATH', 'NASF_NR', 'NASF_PHY', 'NASF_PSY', 'NASF_SOC', 'NASF_OTH',
    'NASF_CLIN_TRIAL', 'NASF_MED']}

GENERAL_COLUMNS = {2019: [
    'YEAR', 'INST_ID', 'INST_NAME', 'SUBMISSION_FLAG',
    'INST_TYPE', 'INST_STATE', 'TOC_CODE', 'EXP_TOT_2018']}

FILTER_VALUES = {
    2019:
    {'SUBMISSION_FLAG': ['Y', None],
     'RRBOX': [1],
     # 'RRBOX':
     # ['1', 'RR_AG', 'RR_BIO', 'RR_COS', 'RR_ENG', 'RR_GEO', 'RR_HLTH',
     # 'RR_MATH', 'RR_NR', 'RR_PHY', 'RR_PSY', 'RR_SOC', 'RR_OTH',
     # 'RR_TFUND'],
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
     }
}
