# Packages importation:
from flask import Flask, session, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
import shutil
import threading

# Files importation:
from analysis.languages_analysis import languages_analysis
from analysis.year_analysis import year_analysis
from analysis.type_analysis import type_analysis
from analysis.evolution_analysis import evolution_analysis
from analysis.periodics_analysis import periodics_analysis
from analysis.keywords_analysis import keywords_analysis
from analysis.citations_analysis import citations_analysis

import data_treatment
import merge_scopus_wos
import extract_metadata
import kml_files_merge
import datetime_capture
import train_test_files_generator

# Global variables:
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')


# Flask constructor:
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


# Home route:
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


# Upload route:
@app.route('/analyzes', methods=['GET', 'POST'])
def analyzes():
    try:
        if request.method == 'POST':
            file = request.files['database']
            save_path = os.path.join(
                UPLOAD_FOLDER, secure_filename(file.filename))
            file.save(save_path)

            str_datetime = datetime_capture.captura_data_e_horario()
            session_id = str(uuid.uuid4())
            session['dataframe_name'] = f'database-{str_datetime}-{session_id}.csv'

            if (os.path.exists(os.path.join(UPLOAD_FOLDER, f'database-{str_datetime}-{session_id}.csv'))):
                os.remove(os.path.join(UPLOAD_FOLDER,
                          f'database-{str_datetime}-{session_id}.csv'))
            else:
                pass

            os.rename(save_path, os.path.join(UPLOAD_FOLDER,
                      f'database-{str_datetime}-{session_id}.csv'))
            dataframe = data_treatment.csv_reading(
                f'database-{str_datetime}-{session_id}.csv')
            dataframe_name = session.get('dataframe_name')
        else:
            dataframe_name = session.get('dataframe_name')
            dataframe = data_treatment.csv_reading(dataframe_name)

        headings, data = data_treatment.data_treatment(dataframe)

        years_json = year_analysis(dataframe)
        languages_json = languages_analysis(dataframe)
        documents_json = type_analysis(dataframe)
        evolutions_json = evolution_analysis(dataframe)
        periodics_json = periodics_analysis(dataframe)
        keywords_json = keywords_analysis(dataframe)
        citations_json = citations_analysis(dataframe)

        threading.Timer(33200, delete_bibliometric_file, args=(dataframe_name,)).start()

        return render_template('upload.html',
                               headings=headings,
                               data=data,
                               years_json=years_json,
                               languages_json=languages_json,
                               documents_json=documents_json,
                               evolutions_json=evolutions_json,
                               periodics_json=periodics_json,
                               keywords_json=keywords_json,
                               citations_json=citations_json)
    except:
        return render_template('error.html')
        


def delete_bibliometric_file(filename):
    if os.path.exists(f'upload/{filename}'):
        os.remove(f'upload/{filename}')


# Merge route:
@app.route('/merge', methods=['GET', 'POST'])
def merge():
    return render_template('merge.html', result_file=False)

# Merged route:


@app.route('/sucessfull_merge', methods=['GET', 'POST'])
def merged():
    try:
        files = request.files.getlist("merge_databases")

        str_datetime = datetime_capture.captura_data_e_horario()
        session_id = str(uuid.uuid4())
        session["merge_upload_folder"] = f'merge-{str_datetime}-{session_id}'

        os.makedirs(f'upload\\{session["merge_upload_folder"]}')

        for file in files:
            if str(file.filename)[-4:] == '.txt':
                file.save(f'upload/{session["merge_upload_folder"]}/wos.txt')
            elif str(file.filename)[-4:] == '.csv':
                file.save(
                    f'upload/{session["merge_upload_folder"]}/scopus.csv')
            else:
                if os.path.exists(f'upload/{session["merge_upload_folder"]}'):
                    shutil.rmtree(f'upload/{session["merge_upload_folder"]}')

                return render_template('merge.html', result_file='not_a_zip')

        merge_scopus_wos.merge_scopus_wos(str_datetime, session_id)

        return render_template('merge.html', result_file=True)
    except:
        if os.path.exists(f'upload/{session["merge_upload_folder"]}'):
            shutil.rmtree(f'upload/{session["merge_upload_folder"]}')

        return render_template('error.html')


# Merged download route:
@app.route('/download_file', methods=['GET'])
def download():
    try:
        download_folder = session.get("merge_upload_folder")
        if download_folder is not None:
            return send_file(
                f'upload/{download_folder}/merged-database.csv',
                mimetype='text/csv',
                download_name='scopus-wos-merged.csv',
                as_attachment=True
            )
        else:
            return render_template('error.html')
    finally:
        threading.Timer(10, delete_merge_folder,
                        args=(download_folder,)).start()


def delete_merge_folder(download_folder):
    if os.path.exists(f'upload/{download_folder}'):
        shutil.rmtree(f'upload/{download_folder}')


# Metadata route:
@app.route('/metadata', methods=['GET', 'POST'])
def metadata():
    return render_template('metadata.html', result_file=False)


# Merged route:
@app.route('/sucessfull_metadata', methods=['GET', 'POST'])
def metadated():
    try:
        files = request.files.getlist("extract_metadata")

        for file in files:
            if str(file.filename)[-4:] == '.zip':
                os.makedirs(r'upload\metadata')
                file.save('upload/metadata/raw-images.zip')
            else:
                return render_template('metadata.html', result_file='not_a_zip')

        extract_metadata.create_dataset_folder()
        extract_metadata.unzip()
        extract_metadata.read_images()
        data = extract_metadata.coordinates()

        headings = ['Image', 'Time', 'Date', 'Latitude', 'Longitude', 'Altitude', 'Latitude Reference',
                    'Longitude Reference', 'Image Pixel Dimensions', 'Image Real Dimensions', 'Image Area']

        return render_template('metadata.html', result_file=True, headings=headings, data=data)
    except:
        if os.path.exists('upload/metadata'):
            shutil.rmtree('upload/metadata')

        return render_template('error.html')
    finally:
        if os.path.exists('upload/dataset'):
            shutil.rmtree('upload/dataset')


# Metadata xlsx files download:
@app.route('/download_xlsx_metadata_file', methods=['GET'])
def download_metadata_xlsx_file():
    try:
        return send_file(
            'upload/metadata/images-metadata.xlsx',
            mimetype='text/csv',
            download_name='images-metadata.xlsx',
            as_attachment=True
        )
    finally:
        threading.Timer(60, delete_metadata_folder).start()


# Metadata kml files download:
@app.route('/download_kml_metadata_file', methods=['GET'])
def download_metadata_kml_file():
    try:
        return send_file(
            'upload/metadata/images-metadata.kml',
            mimetype='application/vnd.google-earth.kml+xml',
            download_name='images-metadata.kml',
            as_attachment=True
        )
    finally:
        threading.Timer(60, delete_metadata_folder).start()


def delete_metadata_folder():
    shutil.rmtree('upload/metadata')


# KML route:
@app.route('/kml_merge', methods=['GET', 'POST'])
def kml_merge():
    return render_template('kml.html', result_file=False)


# KML merged route:
@app.route('/sucessfull_kml', methods=['GET', 'POST'])
def kml_merged():
    files = request.files.getlist("merge_kml_files")

    kml_files_merge.create_kml_folder()

    for aux, file in enumerate(files):
        if str(file.filename)[-4:] == '.kml':
            file.save(f'upload/kml/kml-file-{aux}.kml')
        else:
            pass

    input_files = []

    all_files = os.listdir(os.path.join(UPLOAD_FOLDER, 'kml'))

    for file in all_files:
        if str(file)[-4:] == '.kml':
            input_files.append(os.path.join(UPLOAD_FOLDER, 'kml', file))
        else:
            pass

    kml_files_merge.concatenate_kml_files(input_files, os.path.join(
        UPLOAD_FOLDER, 'kml', 'merged-kml-file.kml'))

    return render_template('kml.html', result_file=True)


# KML concatenated file download:
@app.route('/download_kml_file', methods=['GET'])
def download_kml_file():
    try:
        return send_file(
            'upload/kml/merged-kml-file.kml',
            mimetype='application/vnd.google-earth.kml+xml',
            download_name='merged-kml-file.kml',
            as_attachment=True
        )
    finally:
        threading.Timer(10, delete_kml_folder).start()


def delete_kml_folder():
    shutil.rmtree('upload/kml')


# Train and test route:
@app.route('/train_test', methods=['GET', 'POST'])
def train_test():
    return render_template('train-test.html', result_file=False)


# Merged route:
@app.route('/sucessfull_serialized', methods=['GET', 'POST'])
def serialized():
    try:
        files = request.files.getlist("serialize_cnn_files")

        os.makedirs(r'upload\to-serialize')

        for file in files:
            if str(file.filename)[-4:] == '.zip':
                file.save('upload/to-serialize/raw-images.zip')
            else:
                pass

        train_test_files_generator.create_dataset_folder()
        train_test_files_generator.unzip()
        train_test_files_generator.train_test_file_split()
        train_test_files_generator.zip_final_files()

        return render_template('train-test.html', result_file=True)
    # except:
    #     if os.path.exists('upload/to-serialize'):
    #         shutil.rmtree('upload/to-serialize')

    #     return render_template('error.html')
    finally:
        if os.path.exists('upload/dataset'):
            shutil.rmtree('upload/dataset')


# Train n test files download:
@app.route('/download_train_test', methods=['GET'])
def download_train_test():
    try:
        return send_file(
            'upload/to-serialize/serialized-train-test-files.zip',
            mimetype='zip',
            download_name='serialized-train-test-files.zip',
            as_attachment=True
        )
    finally:
        threading.Timer(10, delete_serializer_folder).start()


def delete_serializer_folder():
    shutil.rmtree('upload/to-serialize')


# Languages route:
@app.route('/languages')
def languages():
    try:
        dataframe_name = session.get('dataframe_name')
        dataframe = data_treatment.csv_reading(dataframe_name)
        languages_json = languages_analysis(dataframe)

        return render_template('analysis/languages.html', languages_json=languages_json)
    except:
        return render_template('error.html')


# Overall execution:
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
