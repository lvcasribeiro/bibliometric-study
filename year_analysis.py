# Packages importation:
import matplotlib.pyplot as pypt
import numpy as np

# Years analysis:
def year_analysis(df):
    years = df['Year'];

    fig, ax = pypt.subplots();
    ax.barh(years.value_counts().index, years.value_counts().values);

    ax.set_xlabel('Publications per year');
    ax.grid(axis='x');

    years_list = list(np.arange(years.values.min() - 1, years.values.max() + 2, 1));
    print(years_list)

    pypt.yticks(years_list);
    pypt.show();
