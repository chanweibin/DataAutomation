import argparse, sys, os
from operator import contains
from ast import arg
from socket import INADDR_LOOPBACK
import pandas as pd
import data_df_repos as dfr
import data_plot_graph as dpg
import data_get_info as dinfo
import io_read_file as iorf
import io_save_file as iosf
from datetime import datetime
from spec import balsaSpec

serNumCol = "Parent4"
emulCol = "Parent3"
funCol = "Parent2"

output_file_loc = os.getcwd() + "\\"
output_file_name = "balsa-testname-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"
output_full_name = output_file_loc + output_file_name
input_file_loc = os.getcwd() + "\\"

scriptName = sys.argv[0]
parser = argparse.ArgumentParser(description=str("Inputing arguments for " + scriptName))
parser.add_argument('-input', metavar="Input file location", help="Source file location")
args = parser.parse_args()

if args.input:
    if args.input.endswith(".xlsx") and args.input.contains("\\"):
        input_full_path = args.input
    elif args.input.endswith(".xlsx"):
        input_full_path = input_file_loc + "\\" + args.input
    else:
        input_xlsx = [x for x in os.listdir(input_file_loc) if x.endswith(".xlsx")][0]
        input_full_path = input_file_loc + "\\" + input_xlsx


if __name__ == "__main__": 
    
    df = iorf.excel_to_dataframe()
    
    df.reset_index(inplace=True)
    df_psup = dfr.keyword_filter_row(df, emulCol, "PowerSupply", True)
    df_load = dfr.keyword_filter_row(df, emulCol, "ELoad", True)
    ###### ======================================================================
    df_load_CR = dfr.keyword_filter_row(df_load, funCol, "ResistanceAccuracy", True)
    df_load_CP = dfr.keyword_filter_row(df_load, funCol, "PowerAccuracy", True)
    df_load_CC = dfr.keyword_filter_row(df_load, funCol, "CurrentAccuracy", True)
    df_load_CV = dfr.keyword_filter_row(df_load, funCol, "VoltageAccuracy", True)

    df_psup_smallCurr = dfr.keyword_filter_row(df_psup, funCol, "SmallCurrent", True)
    df_psup_CC = dfr.keyword_filter_row(df_psup, funCol, "CurrentAccuracy", True)
    df_psup_CV = dfr.keyword_filter_row(df_psup, funCol, "VoltageAccuracy", True)
    ###### ======================================================================
    df_load_CR_prog = dfr.keyword_filter_row(df_load_CR, "Name", "Prog")
    df_load_CP_prog = dfr.keyword_filter_row(df_load_CP, "Name", "Prog")
    df_load_CC_prog = dfr.keyword_filter_row(df_load_CC, "Name", "Prog")
    df_load_CV_prog = dfr.keyword_filter_row(df_load_CV, "Name", "Prog")

    df_load_CP_rdbk = dfr.keyword_filter_row(df_load_CP, "Name", "Rdbk")
    df_load_CC_rdbk = dfr.keyword_filter_row(df_load_CC, "Name", "Rdbk")
    df_load_CV_rdbk = dfr.keyword_filter_row(df_load_CV, "Name", "Rdbk")

    df_psup_CC_prog = dfr.keyword_filter_row(df_psup_CC, "Name", "Prog")
    df_psup_CV_prog = dfr.keyword_filter_row(df_psup_CV, "Name", "Prog")

    df_psup_CC_rdbk = dfr.keyword_filter_row(df_psup_CC, "Name", "Rdbk")
    df_psup_CV_rdbk = dfr.keyword_filter_row(df_psup_CV, "Name", "Rdbk")
    
    df_psup_typical = df_psup.drop(pd.concat([df_psup_smallCurr, df_psup_CC, df_psup_CV]).index)
    df_load_typical = df_load.drop(pd.concat([df_load_CR, df_load_CP, df_load_CC, df_load_CV]).index)
    
    df_list = [df_load_CR_prog,df_load_CP_prog,df_load_CC_prog,df_load_CV_prog,
              df_load_CP_rdbk,df_load_CC_rdbk,df_load_CV_rdbk,df_load_typical,
              df_psup_smallCurr, df_psup_CC_prog, df_psup_CV_prog,df_psup_CC_rdbk,
              df_psup_CV_rdbk, df_psup_typical]
        

    # iosf.create_excel_file(output_full_name)
    df_FULL = pd.DataFrame()
    for df_test in df_list:
        df_test = dfr.derive_range_nominal(df_test) # TODO: plan to use for spec calculation
        cols = dfr.keyword_filter_columns_name(df_test, "raw")
        df_test = dfr.derive_mean(df_test, cols)
        df_test = dfr.derive_std(df_test, cols)
        
        
        # * sorting dataframe
        if df_test[funCol].str.contains("PowerAccuracy").any():
            df_test = dfr.sort_on_cols(df_test, ["Range", "Power", "Voltage", "Current"])
        if df_test["Parent2"].str.contains("ResistanceAccuracy").any():
            df_test = dfr.sort_on_cols(df_test, ["Range", "Resistance", "Voltage", "Current"])
        if df_test["Parent2"].str.contains("VoltageAccuracy").any():
            df_test = dfr.sort_on_cols(df_test, ["Range", "Voltage", "Current"])
        if df_test["Parent2"].str.contains("CurrentAccuracy").any():
            df_test = dfr.sort_on_cols(df_test, ["Range", "Current", "Voltage"])
        
        df_test.drop_duplicates("Name", inplace=True)
        
        
        df_FULL = pd.concat([df_FULL, df_test]) #! comment this for sheet per df
        # iosf.append_to_sheet(df_test, output_full_name, 'test') #! uncomment this for sheet per df
    iosf.dataframe_to_excel(df_FULL, output_full_name) #! comment this for sheet per df
    print("done...")
    