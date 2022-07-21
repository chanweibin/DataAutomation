import pandas as pd 
import os, sys

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
    return pd.read_excel(full_file_path)



def xml_to_dataframe(full_file_path):
    return pd.read_xml(full_file_path)



