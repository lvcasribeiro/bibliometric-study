# Packages importation:
import matplotlib.pyplot as pypt

# Keyword analysis:
def keywords_analysis(df):
    df['Index Keywords'] = df['Index Keywords'].astype(str);

    # Removes an specific word, if necessary:
    df = df[~df['Index Keywords'].str.contains('Nan', case=False)];

    keywords = df['Index Keywords'].str.split('; ', expand=True).stack().value_counts()[:20];
    keywords.index = keywords.index.str.title();

    pypt.figure(figsize=(8, 5));
    pypt.barh(keywords.index[:20], keywords.values[:20]);
    pypt.gca().invert_yaxis();
    pypt.xlabel('Occurrence');
    pypt.grid(axis='x', zorder=1);
    # pypt.show();

    keywords_json = keywords.to_dict();

    return keywords_json