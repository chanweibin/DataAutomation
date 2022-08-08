import pandas as pd 
import os, sys
from openpyxl import Workbook, load_workbook

# * =============================================== Sanity Check ==============================================

def loc_sanity_test(input_loc, output_loc):
    
    try:
        if not os.path.exists(input_loc):
            os.makedirs(input_loc)
        if not os.path.exists(output_loc):
            os.makedirs(output_loc)

    except Exception as e:
        raise Exception("Error at check_file_loc : " + str(e))



# * ================================================ Obtain DF ================================================

def csv_to_dataframe(full_file_path):
    return pd.read_csv(full_file_path)



def excel_to_dataframe(full_file_path):
    file_name = full_file_path.split("\\")[-1]
    file_loc = full_file_path.rstrip(file_name)
    
    if not file_name.endswith(".xlsx"):
        print ("Please give full path to file! ")
        sys.exit(1)
        
    os.chdir(file_loc)
    xls = pd.ExcelFile(full_file_path, engine="openpyxl")
    df = pd.read_excel(xls, 0)
    
    return df



def xml_to_dataframe(full_file_path):
    return pd.read_xml(full_file_path)








