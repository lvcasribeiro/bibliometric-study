# Packages importation:
import matplotlib.pyplot as pypt

# Evolution per year analysis:
def evolution_analysis(df):
    evolution = df['Year'].value_counts().sort_index();

    ax = df['Year'].value_counts().sort_index().plot(kind='line');
    ax.set_xticks(range(int(df['Year'].min()), int(df['Year'].max())+1));
    
    pypt.ylabel('Publications');

    pypt.xticks(rotation='vertical');
    pypt.grid(True);
    # pypt.show();

    evolutions_json = evolution.to_dict();

    return evolutions_json
