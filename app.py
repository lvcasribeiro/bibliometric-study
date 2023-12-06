# Packages importation:
from flask import Flask, session, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import boto3
import uuid
import requests
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
import datetime_capture

# Global variables:
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
CHATPDF_API_KEY = 'sec_MwsqofZUKMBJEqS51CAojgb008k1Dbjw'
UPLOAD_API_URL = 'https://api.chatpdf.com/v1/sources/add-file'
ASK_API_URL = 'https://api.chatpdf.com/v1/chats/message'


# Flask constructor:
app = Flask(__name__)
app.secret_key = 'LUCAXRIBEIRINHO'


# Home route:
@app.route('/')
def home():
    return render_template('index.html')


# Bucket S3:
s3 = boto3.client('s3', aws_access_key_id='AKIA4MG5PQ7GSL7GVDAF',
                  aws_secret_access_key='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')


def create_s3_folder(bucket_name, s3_folder_name):
    try:
        # Adicione uma barra no final do nome da pasta para indicar que é uma pasta
        if not s3_folder_name.endswith('/'):
            s3_folder_name += '/'
        # Crie um objeto vazio representando a pasta
        s3.put_object(Bucket=bucket_name, Key=s3_folder_name)
        return True
    except Exception as e:
        return False


def delete_s3_folder(bucket_name, s3_folder_name):
    try:
        objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])

        s3.delete_object(Bucket=bucket_name, Key=s3_folder_name)

        return True
    except Exception as e:
        return False


def upload_file_to_s3(file, bucket_name, s3_file_name):
    try:
        s3.upload_fileobj(file, bucket_name, s3_file_name)
        return True
    except Exception as e:
        return False


def delete_file_from_s3(bucket_name, s3_file_name):
    try:
        s3.delete_object(Bucket=bucket_name, Key=s3_file_name)
        return True
    except Exception as e:
        return False


def get_file_object_from_s3(bucket_name, s3_file_name):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=s3_file_name)
        return response['Body']
    except Exception as e:
        return None


# Upload route:
@app.route('/analyzes', methods=['GET', 'POST'])
def analyzes():
    try:
        if request.method == 'POST':
            file = request.files['database']
            # save_path = os.path.join(
            #     UPLOAD_FOLDER, secure_filename(file.filename))
            # file.save(save_path)

            str_datetime = datetime_capture.captura_data_e_horario()
            session_id = str(uuid.uuid4())
            session['dataframe_name'] = f'database-{str_datetime}-{session_id}.csv'

            upload_file_to_s3(
                file, 'bibliometric-analyzes-bucket', session["dataframe_name"])

            # if (os.path.exists(os.path.join(UPLOAD_FOLDER, f'database-{str_datetime}-{session_id}.csv'))):
            #     os.remove(os.path.join(UPLOAD_FOLDER,
            #               f'database-{str_datetime}-{session_id}.csv'))
            # else:
            #     pass

            # os.rename(save_path, os.path.join(UPLOAD_FOLDER,
            #           f'database-{str_datetime}-{session_id}.csv'))
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

        threading.Timer(3600, delete_bibliometric_file,
                        args=(dataframe_name,)).start()

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
    # if os.path.exists(f'upload/{filename}'):
    #     os.remove(f'upload/{filename}')

    delete_file_from_s3('bibliometric-analyzes-bucket', filename)


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

        # os.makedirs(f'upload\\{session["merge_upload_folder"]}')

        create_s3_folder('bibliometric-analyzes-bucket',
                         session["merge_upload_folder"])

        for file in files:
            if len(files) > 1:
                if str(file.filename)[-4:] == '.txt':
                    # file.save(f'upload/{session["merge_upload_folder"]}/wos.txt')
                    upload_file_to_s3(
                        file, 'bibliometric-analyzes-bucket', f'{session["merge_upload_folder"]}/wos.txt')
                elif str(file.filename)[-4:] == '.csv':
                    # file.save(f'upload/{session["merge_upload_folder"]}/scopus.csv')
                    upload_file_to_s3(file, 'bibliometric-analyzes-bucket',
                                      f'{session["merge_upload_folder"]}/scopus.csv')
                else:
                    # if os.path.exists(f'upload/{session["merge_upload_folder"]}'):
                    #     shutil.rmtree(f'upload/{session["merge_upload_folder"]}')
                    delete_s3_folder('bibliometric-analyzes-bucket',
                                     session["merge_upload_folder"])
                    return render_template('merge.html', result_file='not_a_zip')
            else:
                # if os.path.exists(f'upload/{session["merge_upload_folder"]}'):
                #     shutil.rmtree(f'upload/{session["merge_upload_folder"]}')
                delete_s3_folder('bibliometric-analyzes-bucket',
                                 session["merge_upload_folder"])
                return render_template('merge.html', result_file='not_a_zip')

        merge_scopus_wos.merge_scopus_wos(str_datetime, session_id)

        return render_template('merge.html', result_file=True)
    except:
        # if os.path.exists(f'upload/{session["merge_upload_folder"]}'):
        #     shutil.rmtree(f'upload/{session["merge_upload_folder"]}')
        delete_s3_folder('bibliometric-analyzes-bucket',
                         session["merge_upload_folder"])

        return render_template('error.html')


# Merged download route:
@app.route('/download_file', methods=['GET'])
def download():
    try:
        download_folder = session.get("merge_upload_folder")
        if download_folder is not None:
            return send_file(
                get_file_object_from_s3(
                    'bibliometric-analyzes-bucket', f'{download_folder}/merged-database.csv'),
                # f'upload/{download_folder}/merged-database.csv',
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
    # if os.path.exists(f'upload/{download_folder}'):
    #     shutil.rmtree(f'upload/{download_folder}')

    delete_s3_folder('bibliometric-analyzes-bucket', download_folder)


# Chat route:
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html', result_file=False)


@app.route('/chat_pdf', methods=['POST'])
def chat_pdf():
    try:
        if 'file' not in request.files:
            return redirect(url_for('index'))

        file = request.files['file']

        if file.filename == '':
            return redirect(url_for('index'))

        if file:
            # Upload file to ChatPDF
            headers = {'x-api-key': CHATPDF_API_KEY}
            files = {'file': (file.filename, file.read())}

            response = requests.post(UPLOAD_API_URL, headers=headers, files=files)

            if response.status_code == 200:
                source_id = response.json()['sourceId']
                # Ask questions using ChatPDF API
                questions = [
                    {
                        'role': 'user',
                        'content': 'What are the main topics of this paper?',
                    },
                    {
                        'role': 'user',
                        'content': 'Can you resume the introduction?',
                    },
                    {
                        'role': 'user',
                        'content': 'What research methods were employed in the study?',
                    },
                    {
                        'role': 'user',
                        'content': 'How does the study contribute to existing knowledge in the field?',
                    },
                    # Add more questions as needed
                ]

                questions_list = ['What are the main topics of this paper?', 'Can you resume the introduction?',
                                'What research methods were employed in the study?', 'How does the study contribute to existing knowledge in the field?']

                data = {'sourceId': source_id, 'messages': questions}
                response = requests.post(ASK_API_URL, headers=headers, json=data)

                if response.status_code == 200:
                    answers = [answer.strip() for answer in response.json()['content'].split('\n') if answer.strip()]
                    print(answers)
                    result = list(zip(questions_list, answers))
                    return render_template('chat.html', result=result, answers=answers, result_file=True)
                else:
                    return f'Error asking questions: {response.status_code} - {response.text}'
            else:
                return f'Error uploading file: {response.status_code} - {response.text}'
    except:
        return render_template('error.html')


# About:
@app.route('/about')
def about():
    return render_template('about.html')


# Statistical analyzes:
@app.route('/statistical')
def statistical():
    return render_template('statistical.html')


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

# Year route:


@app.route('/year')
def year():
    try:
        dataframe_name = session.get('dataframe_name')
        dataframe = data_treatment.csv_reading(dataframe_name)
        years_json = year_analysis(dataframe)

        return render_template('analysis/year.html', years_json=years_json)
    except:
        return render_template('error.html')


# Evolution route:
@app.route('/evolution')
def evolution():
    try:
        dataframe_name = session.get('dataframe_name')
        dataframe = data_treatment.csv_reading(dataframe_name)
        evolutions_json = evolution_analysis(dataframe)

        return render_template('analysis/evolution_per_year.html', evolutions_json=evolutions_json)
    except:
        return render_template('error.html')


# Evolution route:
@app.route('/periodic')
def periodic():
    try:
        dataframe_name = session.get('dataframe_name')
        dataframe = data_treatment.csv_reading(dataframe_name)
        periodics_json = periodics_analysis(dataframe)

        return render_template('analysis/periodics.html', periodics_json=periodics_json)
    except:
        return render_template('error.html')


# Evolution route:
@app.route('/citation')
def citation():
    try:
        dataframe_name = session.get('dataframe_name')
        dataframe = data_treatment.csv_reading(dataframe_name)
        citations_json = citations_analysis(dataframe)

        return render_template('analysis/citations.html', citations_json=citations_json)
    except:
        return render_template('error.html')


# Evolution route:
@app.route('/keyword')
def keyword():
    try:
        dataframe_name = session.get('dataframe_name')
        dataframe = data_treatment.csv_reading(dataframe_name)
        keywords_json = keywords_analysis(dataframe)

        return render_template('analysis/keywords.html', keywords_json=keywords_json)
    except:
        return render_template('error.html')

# Evolution route:


@app.route('/document')
def document():
    try:
        dataframe_name = session.get('dataframe_name')
        dataframe = data_treatment.csv_reading(dataframe_name)
        documents_json = type_analysis(dataframe)

        return render_template('analysis/documents.html', documents_json=documents_json)
    except:
        return render_template('error.html')


# Overall execution:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
