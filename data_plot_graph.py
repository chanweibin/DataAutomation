import matplotlib.pyplot as plt
from numpy import true_divide # plt.savefig()
import pandas as pd
import data_df_repos as dfr


#! ----------------------------------- FILE SETTINGS -----------------------------------
# * load df for experiment purpose only 
# df = pd.read_excel("C:\\Users\\weichan\\Downloads\\BalsaIssue\\LPQ2\\SlotTest\\testing.xlsx").head(10)
# print(df)
# df.dropna(inplace=True)

#! ----------------------------------- FILE SETTINGS -----------------------------------

# TODO: use raw data, UL, LL to plot data, add sigma, UCL, LCL


def plot_raw_graph(df, filename):
    col_list = dfr.keywords_filter_columns_name(df, ["LowerLimit","UpperLimit"])
    col_list.extend(dfr.keyword_filter_columns_name(df, "raw"))
    # df = dfr.keyword_filter_row(df, "Parent3", "CH1")
    df.set_index("Name", inplace=True)
    df = df[col_list].astype(float)
    df.plot()
    filename += ".png"
    plt.show()
    plt.savefig(filename)
    
# plot_raw_graph(df, "test")