# Packages importation:
import pandas as pypd
import os

# Global variables:
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload');

# .csv file reading:
def csv_reading():
    # Reading the .csv scopus file:
    scopus_dataframe = pypd.read_csv(os.path.join(UPLOAD_FOLDER, 'database.csv'));

    return scopus_dataframe


# .csv file treatment:
def data_treatment(dataframe):
    headings = ['Authors', 'Title', 'Year', 'Publisher', 'Conference name', 'Location', 'Language', 'Document'];

    dataframe = dataframe[['Authors', 'Title', 'Year', 'Publisher', 'Conference name', 'Conference location', 'Language of Original Document', 'Document Type']].copy();
    dataframe = dataframe.fillna(value='---')

    authors = dataframe['Authors'].values.tolist();
    title = dataframe['Title'].values.tolist();
    year = dataframe['Year'].values.tolist();
    pub = dataframe['Publisher'].values.tolist();
    conf_name = dataframe['Conference name'].values.tolist();
    conf_loc = dataframe['Conference location'].values.tolist();
    lang = dataframe['Language of Original Document'].values.tolist();
    doc_type = dataframe['Document Type'].values.tolist();
    
    data = [];

    for row in range(0, len(dataframe)):
        data.append((authors[row], title[row], year[row], pub[row], conf_name[row], conf_loc[row], lang[row], doc_type[row]));

    return headings, data
