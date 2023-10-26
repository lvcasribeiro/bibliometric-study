# Packages importation:
from scopus_of_science import SOS
import os

# Global variables:
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')

# Merge of scopus and wos databases:
def merge_scopus_wos(str_datetime, session_id):
    s = SOS(sco=f"upload/merge-{str_datetime}-{session_id}/scopus.csv",
            wos=f"upload/merge-{str_datetime}-{session_id}/wos.txt")

    data = s.get()

    data.to_csv(
        f"upload/merge-{str_datetime}-{session_id}/merged-database.csv", index=False)
