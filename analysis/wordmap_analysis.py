# Packages importation:
import matplotlib.pyplot as pypt
from wordcloud import WordCloud

# Word cloud analysis (based on keywords in the body of the document):
def wordmap_analysis(df):
    df['Index Keywords'] = df['Index Keywords'].astype(str);

    text = ';'.join(df['Index Keywords']);
    wordcloud = WordCloud(width=800, height=800, background_color='white').generate(text);

    pypt.figure(figsize=(8, 8));
    pypt.imshow(wordcloud);
    pypt.axis('off');
    pypt.show();
