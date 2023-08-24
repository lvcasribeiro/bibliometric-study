# Packages importation:
import pandas as pypd

# Files importation:
import analysis.languages_analysis as languages_analysis
import analysis.year_analysis as year_analysis
import analysis.evolution_analysis as evolution_analysis
import analysis.type_analysis as type_analysis
import analysis.wordmap_analysis as wordmap_analysis
import analysis.keywords_analysis as keywords_analysis
import analysis.periodics_analysis as periodics_analysis
import analysis.citations_analysis as citations_analysis

# Reading the .csv scopus file:
scopus_dataframe = pypd.read_csv(r'C:\Users\lucas\Downloads\scopus-193.csv');

# Overall execution:
if __name__ == '__main__':
    languages_analysis.languages_analysis(scopus_dataframe);
    year_analysis.year_analysis(scopus_dataframe);
    evolution_analysis.evolution_analysis(scopus_dataframe);
    type_analysis.type_analysis(scopus_dataframe);
    wordmap_analysis.wordmap_analysis(scopus_dataframe);
    keywords_analysis.keywords_analysis(scopus_dataframe);
    periodics_analysis.periodics_analysis(scopus_dataframe);
    citations_analysis.citations_analysis(scopus_dataframe);
