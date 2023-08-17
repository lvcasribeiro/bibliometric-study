# Packages importation:
import pandas as pypd

# Files importation:
import languages_analysis

# Reading the .csv file:
scopus_dataframe = pypd.read_csv(r'C:\Users\lucas\Downloads\scopus-193.csv');

# Overall execution:
if __name__ == '__main__':
    languages_analysis.languages_analysis(scopus_dataframe);
