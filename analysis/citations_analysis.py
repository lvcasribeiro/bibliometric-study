# Packages importation:
import matplotlib.pyplot as pypt
import textwrap

# Citations analysis:
def citations_analysis(df):
    paper_citations = df.groupby("Title")["Cited by"].sum();

    top_papers = paper_citations.sort_values(ascending=False)[:50];

    # Remove duplicated papers, if necessary:
    # remove_articles = [""];
    # top_papers = top_papers[~top_papers.index.isin(remove_articles)];

    fig, ax = pypt.subplots(figsize=(10, 6));
    bar_plot = ax.barh(top_papers.index, top_papers.values, height=0.9);

    ax.set_xlabel("Citations", fontsize=12);
    yticklabels = [textwrap.fill(paper, width=70) for paper in top_papers.index];
    yticklabels = [label.replace('\n', ' \n') for label in yticklabels];
    yticks_pos = range(len(yticklabels));
    ax.set_yticks(yticks_pos);
    ax.set_yticklabels(yticklabels);
    ax.grid(axis='x');
    # pypt.show();

    citations_json = top_papers.to_dict();

    for key, value in citations_json.items():
        try:
            citations_json[key] = int(value)
        except ValueError:
            pass

    return citations_json
