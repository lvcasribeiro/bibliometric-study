# Packages importation:
from scopus_of_science import SOS
import os

# Global variables:
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload');

# Merge of scopus and wos databases:
def merge_scopus_wos():
    s = SOS(sco="upload/scopus.csv", wos="upload/wos.txt");

    data = s.get();

    if(os.path.exists(os.path.join(UPLOAD_FOLDER, 'database.csv'))):
        os.remove(os.path.join(UPLOAD_FOLDER, 'database.csv'));
    else:
        pass;
    
    data.to_csv("upload/database.csv", index=False);
