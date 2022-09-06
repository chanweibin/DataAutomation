import argparse
import os
import re
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import data_df_repos as dfr
import data_get_info as info
import io_read_file as iorf
import io_save_file as iosf


#! ----------------------------------- FILE SETTINsGS -----------------------------------
# TODO: IO file settings, currently not in use
user:str = 'weichan'
csv_file_loc = os.getcwd() + "\\"
output_file_loc = os.getcwd() + "\\"
output_file_name = "balsa-testname-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"
output_full_path = output_file_loc + output_file_name

# * dataFrame settings
compiledresultDF:pd.DataFrame = pd.DataFrame()

# * test and unit information
serNumCol:str = "Parent4"
emulCol:str = "Parent3"
funCol:str = "Parent2"
#! ----------------------------------- FILE SETTINGS -----------------------------------



parser = argparse.ArgumentParser(description="This script helps to append csv file(s) into compiled excel sheet")
parser.add_argument('-icsv', metavar="Input CSV file location", help="CSV files folder location")
parser.add_argument('-oloc', metavar="Output file location", help="Location of file data to add in")
parser.add_argument('-ofile', metavar="Output file name")
parser.add_argument('-ixl', metavar="Input excel file name(s), split with \',\' if more than 1 file")
parser.add_argument('-args1', metavar="Column1 Name", default="Name")
parser.add_argument('-args2', metavar="Column2 Name", default="Result")
parser.add_argument('-args3', metavar="Column3 Name", default="PercentSpec")
args = parser.parse_args()

print(sys.argv)
    
if args.icsv:
    csv_file_loc = args.icsv
else:
    pass # raise Exception("Please insert raw data file location")

if args.oloc:
    output_file_loc = args.oloc
# else:
    # raise Error("Please insert excel file")

if args.ofile:
    output_file_name = args.ofile
    
    
if args.ixl:
    input_excel_list:str = args.ixl.split(',')
    for input_excel in input_excel_list:
        if not input_excel.endswith('.xlsx'):
            input_excel += '.xlsx'
else:
    os.chdir(output_file_loc)
    input_excel_list:str = [x for x in os.listdir(output_file_loc) if x.endswith(".xlsx")]
    


args1, args2, args3 = args.args1, args.args2, args.args3


def read_Excel() -> list[pd.DataFrame]:
    df_list = []
    global output_full_path
    output_full_path = output_file_loc + "\\" + output_file_name
    os.chdir(output_file_loc)
    for excel in input_excel_list:
        df:pd.DataFrame = iorf.excel_to_dataframe(output_file_loc + "\\" + excel)
        df_list.append(df)
        
    return df_list
        
        
        
def merge_dataframes(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    
    compileDF = df_list[0]
    df_list.pop(0)
    for file in range(len(df_list)):
        compileDF = dfr.merge_on(compileDF, df_list[file], args1, False)
    return compileDF

    
    
    
    
    
if __name__ == "__main__":
    df_list: list[pd.DataFrame] = read_Excel()
    df_full: pd.DataFrame = merge_dataframes(df_list)
    iosf.dataframe_to_excel(df_full, output_full_path)
    
