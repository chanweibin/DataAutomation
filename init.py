import argparse, sys, os
import pandas as pd
import data_df_repos as dfr
import data_plot_graph as dpg
import data_get_info as dinfo
import io_read_file as iorf
import io_save_file as iosf
from datetime import datetime


# * property
input_file_loc = os.getcwd() + "\\"
output_file_loc = os.getcwd() + "\\"
output_file_name = "balsa-testname-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"
output_full_name = output_file_loc + output_file_name

# * test and unit information
serNumCol = "Parent4"
emulCol = "Parent3"
funCol = "Parent2"





scriptName = sys.argv[0]
parser = argparse.ArgumentParser(description=str("Inputing arguments for " + scriptName))
parser.add_argument('-input', metavar="Input file location", help="Source file location")
parser.add_argument('-output', metavar="Target file location", help="Location of file data to add in")
parser.add_argument('-args1', metavar="Column1 Name", default="Name")
parser.add_argument('-args2', metavar="Column2 Name", default="Result")
parser.add_argument('-args3', metavar="Column3 Name", default="PercentSpec")
parser.add_argument('-args4', metavar="Column4 Name", default="UpperLimit,LowerLimit,Parent3,Parent2") # those col that only occurs 1 time
parser.add_argument('-args5', metavar="Column5 Name", default="Parent4") # cols that occur multiple times
parser.add_argument('-pt', metavar="Sheet Name", default="Sheet1", help="Temp workaround")
parser.add_argument('-colname', metavar="Choose SN name, unit || filename", default="unit")

args = parser.parse_args()


if args.input:
    input_file_loc = args.input

if args.output:
    output_file_loc = args.output

args1, args2, args3 = args.args1, args.args2, args.args3
args4 = []
if args.args4:
    args4 = args.args4.split(",")

if args.colname:
    colname = args.colname


def balsa_dA():
    try:
        resultDFList = [] #list
        
        files = [x for x in os.listdir(input_file_loc) if x.endswith(".csv")]
        if not files:
            print(f"File not found in the folder: {input_file_loc} ...\nExitting!")
            sys.exit(1)

        for file in range(len(files)):
            os.chdir(input_file_loc)
            print(f"Extracting data from [{files[file]}] ...")
        
            rawDF = pd.read_csv(files[file])
            resultDFList.append(rawDF)
            
            if colname == "unit":
                sn = dinfo.get_SN(rawDF[serNumCol]) 
                resultName = "raw " + sn
                percentName = "% " + sn
                del(rawDF)
            else:
                name = files[file].split(".csv")[0]
                resultName = "raw " + name
                percentName = "% " + name
                
            argslist = [args1, args2, args3]
            if args4:
                argslist.extend(args4)
            resultDFList[file] = dfr.keyword_filter_column(resultDFList[file], argslist)
            resultDFList[file] = resultDFList[file].rename(columns={args2:resultName, args3:percentName})
            
            
            # * compile df list into signle df
            compileDF = resultDFList[0]
            for file in range(len(files)-1):
                compileDF = dfr.merge_on(compileDF, resultDFList[file+1], args1) 
            
                

            # * rearrage df
            compileDF.sort_index(axis=1, inplace=True) # sort column
            compileDF.sort_values(["Parent3","Name"], ascending=True, inplace=True, na_position="first") # sort rows

            compileDF.set_index(args1, inplace=True)
            
            return compileDF 

    except:
        pass

if __name__ == "__main__":
    iorf.loc_sanity_test(input_file_loc, output_file_loc)
    df = balsa_dA()
    
    
    df_psup = dfr.keyword_filter_row(df, "Parent3", "PowerSupply")
    df_load = dfr.keyword_filter_row(df, "Parent3", "ELoad")
    ###### ======================================================================
    df_load_CR = dfr.keyword_filter_row(df_load, "Parent2", "ResistanceAccuracy")
    df_load_CP = dfr.keyword_filter_row(df_load, "Parent2", "PowerAccuracy")
    df_load_CC = dfr.keyword_filter_row(df_load, "Parent2", "CurrentAccuracy")
    df_load_CV = dfr.keyword_filter_row(df_load, "Parent2", "VoltageAccuracy")

    df_psup_CC = dfr.keyword_filter_row(df_psup, "Parent2", "CurrentAccuracy")
    df_psup_CV = dfr.keyword_filter_row(df_psup, "Parent2", "VoltageAccuracy")
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
    
    df_list = [df_load_CR_prog,df_load_CP_prog,df_load_CC_prog,df_load_CV_prog,
              df_load_CP_rdbk,df_load_CC_rdbk,df_load_CV_rdbk, df_psup_CC_prog,
              df_psup_CV_prog,df_psup_CC_rdbk,df_psup_CV_rdbk]
        


for df_test in df_list:
    df_test = dfr.derive_range_nominal(df_test)
    df_test = dfr.derive_mean(df_test, dfr.keyword_filter_columns_name("raw"))
    df_test = dfr.derive_std(df_test, dfr.keyword_filter_columns_name("raw"))
    iosf.append_to_sheet(df_test, output_full_name, df_test.index(df_test))
    print("done...")
    