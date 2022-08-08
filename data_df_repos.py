from matplotlib.pyplot import axis
import pandas as pd 
import re, sys


#! ----------------------------------- FILE SETTINGS -----------------------------------
pd.options.mode.chained_assignment = None
# * load df for experiment purpose only 
# df = pd.read_excel("C:\\Users\\weichan\\Downloads\\BalsaIssue\\LPQ2\\SlotTest\\testing.xlsx")
# print(df)
# df.dropna(inplace=True)

#! ----------------------------------- FILE SETTINGS -----------------------------------


#* ----------------------------------- Filtering Data -----------------------------------


def keyword_filter_column(df, keyword_list):
    """Filter dataframe based on column

    Args:
        df (dataframe): dataframe to read
        keyword_list (list): list of column/label

    Returns:
        dataframe: Filtered Dataframe
    """
    return df[keyword_list]



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



def keywords_filter_columns_name(df, keywords_list):
    """Return list of columns name that matach keyword

    Args:
        df (dataframe)
        keyword_list (string list ): keyword to filter dataframe columns

    Returns:
        list: list that contains keyword
    """
    return [col for col in df.columns if col in keywords_list]



def keyword_filter_columns_name(df, keyword):
    return [col for col in df.columns if keyword in col]



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
        return print("Rename failed, namelist length not the same ... ")
    
    for i in range(len(old_namelist)):
        df = df.rename(columns={old_namelist[i]:new_namelist[i]})
        
    return df




#* ----------------------------------- Merge & Sort Data -----------------------------------

# TODO: merge on
def merge_on(df_full, df, col):
    df_full = df_full.merge(df, on=col, how="outer", suffixes=('','_y'))
    df_full.drop(df_full.filter(regex='_y$').columns.tolist(), axis=1, inplace=True)
    return df_full
    


# TODO: merge on columns
# TODO: merge on rows
# TODO: sort on index
# TODO: sort on cols
# TODO: set/reset index # not recommended to use in merge, prefer merge_on






#* ----------------------------------- Deriving Data -----------------------------------

def derive_new_column_formula(df, lookup_column, new_column, formula): #! not ready to be used
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
    df["Mean"] = df.drop(df.columns.difference(result_list) , axis=1).astype(float).mean(axis=1, numeric_only=True)
    return df



def derive_std(df, result_list):
    """Derive stdev of result list

    Args:
        df (Dataframe): Dataframe with result list 
        result_list (String list): List of columns to calculate stdev

    Returns:
        Dataframe: Dataframe with stdev
    """
    df["Stdev"] = df.drop(df.columns.difference(result_list) , axis=1).astype(float).std(axis=1, numeric_only=True)
    return df



def derive_test_settings(df, column_label="Name"):
    """Split Name to get useful info 
    (Source file naming need to follow Balsa test result pattern)

    Args:
        df (dataframe): dataframe with info
        column_label (str, optional): Name of column label. Defaults to "Name".

    Returns:
        dataframe: Dataframe with more analysed info
    """
    df_new = df[column_label].str.split("_|-")
    df["Range"] = df_new.str.get(1)
    df["VI"] = df_new.str.get(-1)
    # df["TestSetting"] = df["Name"].str.split("_|-")
    return df



def derive_range(df):
    """Get testing range for each test points

    Args:
        df (dataframe)

    Returns:
        dataframe: Udpated dataframe with test range
    """
    df_TestSetting = derive_test_settings(df)
    df["Range"] = df_TestSetting["Range"].str.extract('(\d+)', expand=False)
    return df


    
def derive_nominal(df):
    """Get nominal(V/I/P/R) for each test points

    Args:
        df (dataframe)
        invert_VI (bool, optional): True if using for CurrentAccuracyTest. Defaults to False.

    Returns:
        dataframe: Dataframe with testing parameters
    """
    df_TestSetting = derive_test_settings(df)
    df_TestSetting["VI"] = df_TestSetting["VI"].str.extract("([0-9]+[.]?[0-9]*[AV]@[0-9]+[.]?[0-9]*[AV])", expand=False).str.split("@")
    
    df["Voltage"] = df_TestSetting["VI"].str.get(0) if "V" in df_TestSetting["VI"].str.get(0).to_string() else df_TestSetting["VI"].str.get(1) #* Get V/I, ?V@?A or
    df["Current"] = df_TestSetting["VI"].str.get(1) if "A" in df_TestSetting["VI"].str.get(1).to_string() else df_TestSetting["VI"].str.get(0) #* ?A@?V
    # if invert_VI:
        # df["Voltage"], df["Current"] = df["Current"], df["Voltage"]
    
    df["Voltage"] = df.Voltage.str.extract('(\d+[.]?[0-9]*)', expand=False)  
    df["Current"] = df.Current.str.extract('(\d+[.]?[0-9]*)', expand=False)
    df["Power"] = df.Voltage.astype(float) * df.Current.astype(float)
    df["Resistance"] = df.Voltage.astype(float) / df.Current.astype(float)    
    
    return df


def derive_range_nominal(df):
    df_nom = derive_nominal(df)
    df_range = derive_range(df)
    
    df = df_nom.merge(df_range)
    df.drop("VI", inplace=True, axis=1)
    
    return df


#! ----------------------------------- EXPERIMENT -----------------------------------


# df_psup = keyword_filter_row(df, "Parent3", "PowerSupply")
# df_load = keyword_filter_row(df, "Parent3", "ELoad")
# ###### ======================================================================
# df_load_CR = keyword_filter_row(df_load, "Parent2", "Resistance")
# df_load_CP = keyword_filter_row(df_load, "Parent2", "Power")
# df_load_CC = keyword_filter_row(df_load, "Parent2", "CurrentAccuracy")
# df_load_CV = keyword_filter_row(df_load, "Parent2", "Voltage")

# # df_psup_CC = keyword_filter_row(df_psup, "Parent2", "Current")
# # df_psup_CV = keyword_filter_row(df_psup, "Parent2", "Voltage")
# ###### ======================================================================
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
# ###### ======================================================================
# a = [df_load_CR_prog, df_load_CP_prog, df_load_CC_prog, df_load_CV_prog, df_psup_CC_prog, df_psup_CV_prog]
# dfn = keywords_filter_columns_name(df, ["LowerLimit","UpperLimit"])
# dfn.extend(keyword_filter_columns_name(df, "Port"))




# print(df.columns)
# print(dfn)


# for i in a:
#     print(250*"-")
#     print(i)
