# Packages importation:
import matplotlib.pyplot as pypt

# Languages analysis:
def languages_analysis(df):
    languages = df['Language of Original Document'].value_counts();

    # Translation to portuguese, if necessary:
    # languages.index = ['Inglês' if lang == 'English' else 'Chinês' if lang == 'Chinese' else 'Coreano' if lang == 'Korean' else lang for lang in languages.index];

    pypt.pie(languages.values, labels=languages.index, autopct='%1.1f%%');
    pypt.show();
