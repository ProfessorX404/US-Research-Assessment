import sys
import pandas as pd



def main():
    print('Data File Path:', sys.argv)
    data = pd.read_csv(str(sys.argv).split()[0])
    
if __name__ == '__main__':
    main()