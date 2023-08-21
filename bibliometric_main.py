# Packages importation:
import pandas as pypd

# Files importation:
import languages_analysis
import year_analysis
import evolution_analysis
import type_analysis
import wordmap_analysis

# Reading the .csv scopus file:
scopus_dataframe = pypd.read_csv(r'C:\Users\lucas\Downloads\scopus-193.csv');

# Overall execution:
if __name__ == '__main__':
    languages_analysis.languages_analysis(scopus_dataframe);
    year_analysis.year_analysis(scopus_dataframe);
    evolution_analysis.evolution_analysis(scopus_dataframe);
    type_analysis.type_analysis(scopus_dataframe);
    wordmap_analysis.wordmap_analysis(scopus_dataframe);
