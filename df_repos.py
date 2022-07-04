from matplotlib.pyplot import axis
import pandas as pd 


#! ----------------------------------- FILE SETTINGS -----------------------------------
# * load df for experiment purpose only 
df = pd.read_excel("C:\\Users\\weichan\\Downloads\\BalsaIssue\\LPQ2\\SlotTest\\Balsa_SlotTest.xlsx")
# print(df)
# df.dropna(inplace=True)

#! ----------------------------------- FILE SETTINGS -----------------------------------


#* ----------------------------------- Filtering Data -----------------------------------


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


def keywords_filter_row(df, column_label, keywords):
    """Filter rows based on multiple keywords

    Args:
        df (dataframe): Dataframe to be filtered
        column_label (string): Lookup column
        keyword (string list): Filter keywords in regex

    Returns:
        dataframe: Dataframe with rows filtered on <column_label> that contains <keyword>
    """
    dfnew = pd.DataFrame()
    for keyword in keywords:
        dfnew = dfnew.append(keyword_filter_row(df, column_label, keyword))
    
    return dfnew

def rename_column_label(df, old_namelist, new_namelist):
    """Rename column Label

    Args:
        df (dataframe): dataframe
        old_namelist (string list): Column label to be changed
        new_namelist (string list): New column label name

    Returns:
        dataframe: Dataframe with updated name
    """
    if (isinstance(old_namelist, str) and isinstance(new_namelist, str)):
        old_namelist.split() #* convert string into list
        new_namelist.split() #* convert string into list
            
    if (len(old_namelist) != len(new_namelist)):
        return print("Rename failed")
    
    for i in range(len(old_namelist)):
        df = df.rename(columns={old_namelist[i]:new_namelist[i]})
        
    return df


#* ----------------------------------- Merge & Sort Data -----------------------------------

# TODO: merge on
def merge_on(df_full, df, on):
    df_full.merge(df, on=on)

# TODO: merge on columns
# TODO: merge on rows
# TODO: sort on index
# TODO: sort on cols
# TODO: set/reset index # not recommended to use in merge, prefer merge_on






#* ----------------------------------- Deriving Data -----------------------------------

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



def derive_mean(df, result_list):
    """Derive mean of result list

    Args:
        df (Dataframe): Dataframe with result list 
        result_list (String list): List of columns to calculate mean

    Returns:
        Dataframe: Dataframe with mean
    """
    df["Mean"] = df.drop(df.columns.difference(result_list) , axis=1).mean(axis=1)
    return df



def derive_std(df, result_list):
    """Derive stdev of result list

    Args:
        df (Dataframe): Dataframe with result list 
        result_list (String list): List of columns to calculate stdev

    Returns:
        Dataframe: Dataframe with stdev
    """
    df["Stdev"] = df.drop(df.columns.difference(result_list) , axis=1).std(axis=1)
    return df



def derive_VI(df):
    df["Voltage"] = df["Name"].str.split("_@")
    return df


#! ----------------------------------- EXPERIMENT -----------------------------------


# df_eload = df[df["Parent3"].str.contains("ELoad", na=False)]
# df_psup = df[df["Parent3"].str.contains("PowerSupply", na=False)]
# dfn = keywords_filter_row(df, ["Port1","Port2","Port3","Port4"])

dfn = derive_VI(df)

print(dfn)

# df_psup = keyword_filter_row(df, "Parent3", "PowerSupply")
# df_load = keyword_filter_row(df, "Parent3", "ELoad")
# df_psup.append(df_load)

# print(df_psup)




# df_load_CR = keyword_filter_row(df_load, "Parent2", "Resistance")
# df_load_CP = keyword_filter_row(df_load, "Parent2", "Power")
# df_load_CC = keyword_filter_row(df_load, "Parent2", "Current")
# df_load_CV = keyword_filter_row(df_load, "Parent2", "Voltage")

# df_psup_CC = keyword_filter_row(df_psup, "Parent2", "Current")
# df_psup_CV = keyword_filter_row(df_psup, "Parent2", "Voltage")




# df_load_CR_prog = keyword_filter_row(df_load_CR, "Name", "Prog")
# df_load_CP_prog = keyword_filter_row(df_load_CP, "Name", "Prog")
# df_load_CC_prog = keyword_filter_row(df_load_CC, "Name", "Prog")
# df_load_CV_prog = keyword_filter_row(df_load_CV, "Name", "Prog")

# df_load_CP_rdbk = keyword_filter_row(df_load_CP, "Name", "Rdbk")
# df_load_CC_rdbk = keyword_filter_row(df_load_CC, "Name", "Rdbk")
# df_load_CV_rdbk = keyword_filter_row(df_load_CV, "Name", "Rdbk")

# df_psup_CC_prog = keyword_filter_row(df_psup_CC, "Name", "Prog")
# df_psup_CV_prog = keyword_filter_row(df_psup_CV, "Name", "Prog")

# df_psup_CC_rdbk = keyword_filter_row(df_psup_CC, "Name", "Rdbk")
# df_psup_CV_rdbk = keyword_filter_row(df_psup_CV, "Name", "Rdbk")

# a = [df_load_CR_prog, df_load_CP_prog, df_load_CC_prog, df_load_CV_prog, df_psup_CC_prog, df_psup_CV_prog]

# for i in a:
#     print(250*"-")
#     print(i)
