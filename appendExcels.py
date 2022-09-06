from msilib.schema import Error
import pandas as pd
import argparse, os, sys
from openpyxl import load_workbook
from datetime import datetime
import io_save_file as iosf
import data_df_repos as dfr

file_loc = os.getcwd()
csv_file_loc = os.getcwd()
output_file_name = "balsa-testname-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"
input_excel_list = [x for x in os.listdir(file_loc) if x.endswith(".xlsx")]
output_full_path = file_loc + "//" + output_file_name

def read_Excel(file):
    os.chdir(file_loc)
    
    xls = pd.ExcelFile(file, engine="openpyxl")
    df = pd.read_excel(xls, 0)
    return df


if __name__ == "__main__":
    df_compile = pd.DataFrame()
    for file in input_excel_list:
        df = read_Excel(file)
        df_compile = dfr.merge_on(df_compile, df, "Name")
        
    iosf.dataframe_to_excel(df_compile, output_full_path)
    
    
    
        
   
    
    