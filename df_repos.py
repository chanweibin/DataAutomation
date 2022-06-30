import pandas as pd 
import re, sys


#! ----------------------------------- FILE SETTINGS -----------------------------------
# * load df for experiment purpose only 
df = pd.read_excel("C:\\Users\\weichan\\Downloads\\BalsaIssue\\LPQ2\\SlotTest\\Balsa_SlotTest.xlsx")
# print(df)
# df.dropna(inplace=True)

#! ----------------------------------- FILE SETTINGS -----------------------------------


def filter_column(df, column_list):
    """Filter dataframe based on column

    Args:
        df (dataframe): dataframe to read
        column_list (list): list of column/label

    Returns:
        dataframe: Filtered Dataframe
    """
    return df[column_list]



def keyword_filter_row(df, column_label, keyword):
    """Filter rows based on keyword

    Args:
        df (dataframe): Dataframe to be filtered
        column_label (string): Lookup column
        keyword (string): Filter keyword in regex

    Returns:
        dataframe: Dataframe with rows filtered on <column_label> that contains <keyword>
    """
    return df[df[column_label].str.contains(keyword, na=False, regex=False)]



def rename_column_label(df, old_namelist, new_namelist):
    """Rename column Label

    Args:
        df (dataframe): dataframe
        old_namelist (string list): Column label to be changed
        new_namelist (string list): New column label name

    Returns:
        dataframe: Dataframe with updated name
    """
    if (len(old_namelist) != len(new_namelist)):
        return print("Rename failed")
    
    for i in range(len(old_namelist)):
        df = df.rename(columns={old_namelist[i]:new_namelist[i]})
        
    return df


# TODO
def merge_on(df_full, df, on):
    df_full.merge(df, on=on)



def derive_new_column(df, lookup_column, new_column, formula):
    """Derive new column based on lookup column

    Args:
        df (dataframe): dataframe to be modify
        lookup_column (string): Lookup column name
        new_column (string): New Column Name
        formula (lambda): Formula to derive new value

    Returns:
        dataframe: New dataframe
    """
    df[new_column] = formula(df[lookup_column])
    return df 



# df_eload = df[df["Parent3"].str.contains("ELoad", na=False)]
# df_psup = df[df["Parent3"].str.contains("PowerSupply", na=False)]
dfn = filter_column(df, ["Parent3","Parent2"])

print(dfn)