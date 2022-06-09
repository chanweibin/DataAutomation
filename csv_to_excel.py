import argparse
import os
import re
import sys
from datetime import datetime
import pandas as pd
import numpy as np
from openpyxl import load_workbook 

import Unit_TestInfo as utif

# TODO: IO file settings, currently not in use
user = 'weichan'
csv_file_loc = os.getcwd() + "\\"
output_file_loc = os.getcwd() + "\\"
output_file_name = "outputfile-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"
output_full_path = output_file_loc + output_file_name

# * dataFrame settings
compiledresultDF = pd.DataFrame()

# * test and unit information
serNumCol = "Parent4"
emulCol = "Parent3"
funCol = "Parent2"

scriptName = sys.argv[0]
parser = argparse.ArgumentParser(description=str("Inputing arguments for " + scriptName))
parser.add_argument('-id', metavar="ID", help="Key in four digit ID")
parser.add_argument('-csv', metavar="CSV", help="CSV files folder location")
parser.add_argument('-output', metavar="Output file location", help="Location of file data to add in")
parser.add_argument('-file', metavar="Output file name")
parser.add_argument('-user', metavar="Username", help="User PC name")
parser.add_argument('-args1', metavar="Column1 Name", default="Name")
parser.add_argument('-args2', metavar="Column2 Name", default="Result")
parser.add_argument('-args3', metavar="Column3 Name", default="PercentSpec")
parser.add_argument('-args4', metavar="Column4 Name", default="UpperLimit,LowerLimit,Parent3,Parent2") # those col that only occurs 1 time
parser.add_argument('-args5', metavar="Column5 Name", default="Parent4") # cols that occur multiple times
parser.add_argument('-pt', metavar="Sheet Name", default="Sheet1", help="Temp workaround")
parser.add_argument('-colname', metavar="Choose SN name, unit || filename", default="unit")

args = parser.parse_args()

if args.id and args.id.isdigit():
    id = int(args.id)
else:
    id = 0
    # TODO: print("ID is null or non-digit, generating ID: {:04d}".format(id))

if args.csv:
    csv_file_loc = args.csv
else:
    pass # TODO: raise Exception("Please insert raw data file location")

if args.output:
    output_file_loc = args.output

if args.file:
    output_file_name = args.file
    if not output_file_name.endswith('.xlsx'):
        output_file_name += '.xlsx'

if args.user:
    user = args.user

if args.pt:
    sheetName = args.pt

args1, args2, args3 = args.args1, args.args2, args.args3
args4 = []
if args.args4:
    args4 = args.args4.split(",")

if args.colname:
    colname = args.colname


def check_file_loc():

    global output_full_path
    
    try:
        if not os.path.exists(csv_file_loc):
            os.makedirs(csv_file_loc)
        if not os.path.exists(output_file_loc):
            os.makedirs(output_file_loc)

        output_full_path = output_file_loc + output_file_name

    except Exception as e:
        raise Exception("Error at check_file_loc : " + str(e))


# ! WIP
def get_test_info(df):

    try:
        if df["Parent3"].str.contains("PowerSupply", na=False).all():
            df["Spec_EMUL"] = "PowerSupply"
            print(df.to_string())
            
            sys.exit(1)
        # elif df["Parent3"].contains("Eload"):
        else:
            df["Spec_EMUL"] = "ELoad"
            print(df.to_string())
            sys.exit(1)
        
        if df["Spec_EMUL"] == "PowerSupply":
            if df["Parent2"].contains("VoltageAccuracyTest"):
                df["Spec_FUNC"] = "VOLT"
            else:
                df["Spec_FUNC"] = "CURR"
        
        sys.exit(1)


        return df

    except Exception as e:
        raise Exception("Error at get_test_info : " + str(e))



def createDataFrame():

    try:
        resultDFList = [] #list

        files = [x for x in os.listdir(csv_file_loc) if x.endswith(".csv")]
        if not files:
            print(f"File not found in the folder: {csv_file_loc} ...\nExitting!")
            sys.exit(1)

        for file in range(len(files)):
            os.chdir(csv_file_loc)
            print(f"Extracting data from [{files[file]}] ...")

            rawDF = pd.read_csv(files[file])
            resultDFList.append(rawDF)

            if colname == "unit":
                sn = utif.get_SN(rawDF[serNumCol]) 
                resultName = "Result " + sn
                percentName = "% " + sn
                del(rawDF)
            else:
                name = files[file].split(".csv")[0]
                resultName = "raw " + name
                percentName = "% " + name

            argslist = [args1, args2, args3]
            if args4:
                argslist.extend(args4)
            resultDFList[file] = resultDFList[file][argslist]

            resultDFList[file] = resultDFList[file].set_index(args1)
            resultDFList[file] = resultDFList[file].rename(columns={args2:resultName, args3:percentName})

        # * compile df list into signle df
        compileDF = resultDFList[0]
        for file in range(len(files)-1):
            compileDF = compileDF.merge(resultDFList[file+1], left_index=True, right_index=True, how="outer", suffixes=('','_y'))
            compileDF.drop(compileDF.filter(regex='_y$').columns.tolist(), axis=1, inplace=True)
        # print("MERGED:"+ compileDF.to_string())
        
        # * rearrage df
        compileDF.sort_index(axis=1, inplace=True) # sort column
        compileDF.sort_values(["Parent3","Parent2","Name"], ascending=True, inplace=True, na_position="first") # sort rows

        # compileDF = get_test_info(compileDF)
    
        return compileDF

    except Exception as e:
        raise Exception("Error at createDataFrame: " + str(e))



def WriteExcel(compiledresultDF):
    try:
        print(f" ================ Output File : {output_file_name} ================ ")
        print(f"File location : {output_full_path}\n")

        print(f"Checking if {output_file_name} exists ...")
        if not os.path.exists(output_full_path):
            print("File does not exist, creating new excel file now ...")
            writer = pd.ExcelWriter(output_full_path, engine='xlsxwriter')
            compiledresultDF.to_excel(writer, sheet_name=sheetName, index=True, header=True)
        # append excel sheet if excel exists
        else:
            print("File exists, appending data to exising file ...")
            excelWorkbook = load_workbook(output_full_path)
            writer = pd.ExcelWriter(output_full_path, engine='openpyxl')
            writer.book = excelWorkbook
            compiledresultDF.to_excel(writer, sheet_name=sheetName, index=True, header=True)
        writer.save()
        print("... done\n")

    except Exception as e:
        raise Exception("Error at WriteExcel: " + str(e))



if __name__ == '__main__':
    try:
        check_file_loc()
        compiledresultDF = createDataFrame()
        WriteExcel(compiledresultDF)
        sys.exit(0)

    except Exception as e:
        print(e)
        sys.exit(1)