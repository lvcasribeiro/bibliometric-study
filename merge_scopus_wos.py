# Packages importation:
from scopus_of_science import SOS
import boto3
import tempfile
import os

# Global variables:
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')

s3 = boto3.client('s3', aws_access_key_id='AKIA4MG5PQ7GSL7GVDAF',
                  aws_secret_access_key='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')

# Merge of scopus and wos databases:
def merge_scopus_wos(str_datetime, session_id):
    scopus_object = s3.get_object(Bucket='bibliometric-analyzes-bucket', Key=f'merge-{str_datetime}-{session_id}/scopus.csv')['Body'].read().decode('utf-8')
    wos_object = s3.get_object(Bucket='bibliometric-analyzes-bucket', Key=f'merge-{str_datetime}-{session_id}/wos.txt')['Body'].read().decode('utf-8')

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv', encoding='utf-8-sig') as scopus_file, tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt', encoding='utf-8-sig') as wos_file:
        scopus_file.write(scopus_object)
        wos_file.write(wos_object)

    try:
        s = SOS(sco=scopus_file.name, wos=wos_file.name)
        merged_data = s.get()

        if not merged_data.empty:
            s3.put_object(Bucket='bibliometric-analyzes-bucket', Key=f'merge-{str_datetime}-{session_id}/merged-database.csv', Body=merged_data.to_csv(index=False))
        else:
            print("O DataFrame merged_data está vazio.")
    finally:
        os.remove(scopus_file.name)
        os.remove(wos_file.name)
