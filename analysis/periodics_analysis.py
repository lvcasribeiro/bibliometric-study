# Packages importation:
import matplotlib.pyplot as pypt
import textwrap

# Periodics analysis:
def periodics_analysis(df):
    df['Source title'] = df['Source title'].astype(str);
    df['Source title'] = df['Source title'].str.lower().str.title();

    study_areas = df['Source title'].value_counts().sort_values(ascending=False)[:10];
    wrapped_labels = ['\n'.join(textwrap.wrap(label, width=75)) for label in study_areas.index];

    pypt.barh(wrapped_labels, study_areas.values);
    pypt.gca().invert_yaxis();
    pypt.xlabel('Ocurrence');
    pypt.grid(axis='x');
    # pypt.show();

    periodics_json = study_areas.to_dict();

    return periodics_json
