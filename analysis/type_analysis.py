# Packages importation:
import matplotlib.pyplot as pypt

# Document type analysis:
def type_analysis(df):
    doc_counts = df["Document Type"].value_counts();

    # Translation to portuguese, if necessary:
    # doc_counts.index = ['Artigo' if lang == 'Article' else 'Artigo de Conferência' if lang == 'Conference paper' else 'Revisão' if lang == 'Review' else 'Capítulo de Livro' if lang == 'Book chapter' else 'Entrevista' if lang == 'Short survey' else 'Revisão de Conferência' if lang == 'Conference review' else 'Artigo de Análise de Dados' if lang == 'Data paper' else lang for lang in doc_counts.index];

    fig, ax = pypt.subplots(figsize=(8, 8));
    ax.pie(doc_counts.values, labels=doc_counts.index, autopct='%1.1f%%');

    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0));
    pypt.title('Document Type');
    pypt.show();
