from pathlib import Path
import sys
from os.path import abspath
import pandas as pd

VALID_COLLUMNS_2019 = [
    'YEAR', 'INST_ID', 'INST_NAME', 'SUBMISSION_FLAG,'
    'INST_TYPE', 'TOC_CODE', 'EXP_TOT_2018', 'NASF_AG', 'NASF_BIO', 'NASF_COS',
    'NASF_ENG', 'NASF_GEO', 'NASF_HLTH', 'NASF_MATH', 'NASF_NR', 'NASF_PHY',
    'NASF_PSY', 'NASF_SOC', 'NASF_OTH', 'NASF_CLIN_TRIAL', 'NASF_MED']

FILTER_VALUES_2019 = {'SUBMISSION_FLAG': ['Y', None], 'RRBOX': ['1', ]}

''' call using this syntax in terminal:
    [python executable] [path of sanitize_data.py] \
        [path of desired CSV to sanitize] \
            [path of desired location and name of CSV]
    ex:./.env/python.exe ./src/sanitize_data.py \
        ./raw_data/facilities_2019_imputed.csv ./data/2019_sanitized.csv
'''


def main():
    print('Data File Path:', abspath(str(sys.argv[1])))
    print('Location Path: ', abspath(str(sys.argv[2])))
    data = pd.read_csv(abspath(str(sys.argv[1])), encoding='ISO-8859-1')
    filepath = Path(str(sys.argv[2]))
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(filepath)


if __name__ == '__main__':
    main()
