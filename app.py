# Packages importation:
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

# Files importation:
from analysis.languages_analysis import languages_analysis
from analysis.year_analysis import year_analysis
from analysis.type_analysis import type_analysis
from analysis.evolution_analysis import evolution_analysis
from analysis.periodics_analysis import periodics_analysis
from analysis.keywords_analysis import keywords_analysis
from analysis.citations_analysis import citations_analysis

import data_treatment

# Global variables:
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload');


# Flask constructor:
app = Flask(__name__);

# Home route:
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


# Upload route:
@app.route('/analyzes', methods=['GET', 'POST'])
def analyzes():
    file = request.files['database'];
    save_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename));
    file.save(save_path);

    if(os.path.exists(os.path.join(UPLOAD_FOLDER, 'database.csv'))):
        os.remove(os.path.join(UPLOAD_FOLDER, 'database.csv'));
    else:
        pass;

    os.rename(save_path, os.path.join(UPLOAD_FOLDER, 'database.csv'));

    dataframe = data_treatment.csv_reading();
    headings, data = data_treatment.data_treatment(dataframe);

    years_json = year_analysis(dataframe);
    languages_json = languages_analysis(dataframe);
    documents_json = type_analysis(dataframe);
    evolutions_json = evolution_analysis(dataframe);
    periodics_json = periodics_analysis(dataframe);
    keywords_json = keywords_analysis(dataframe);
    citations_json = citations_analysis(dataframe);
    
    return render_template('upload.html', 
                           headings=headings, 
                           data=data, years_json=years_json, 
                           languages_json=languages_json, 
                           documents_json=documents_json, 
                           evolutions_json=evolutions_json, 
                           periodics_json=periodics_json, 
                           keywords_json=keywords_json,
                           citations_json=citations_json)


# Overall execution:
if __name__ == '__main__':
    app.run(debug=True);
