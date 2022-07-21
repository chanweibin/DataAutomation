from msilib.schema import Error
import pandas as pd
import argparse, os, sys
from openpyxl import load_workbook
from datetime import datetime
import io_save_file as iosf

file_loc = os.getcwd()
csv_file_loc = os.getcwd()
output_file_name = ("balsa-testname" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx").split(',')


parser = argparse.ArgumentParser(description="This script helps to append csv file(s) into compiled excel sheet")
parser.add_argument('-icsv', metavar="Input CSV file location", help="CSV files folder location")
parser.add_argument('-oloc', metavar="Output file location", help="Location of file data to add in")
parser.add_argument('-ofile', metavar="Output file name")
parser.add_argument('-ixl', metavar="Input excel file name(s), split with \',\' if more than 1 file")
parser.add_argument('-args1', metavar="Column1 Name", default="Name")
parser.add_argument('-args2', metavar="Column2 Name", default="Result")
parser.add_argument('-args3', metavar="Column3 Name", default="PercentSpec")
parser.add_argument('-append', metavar="[True|False]", help="Whether to append multiple excel to different sheets")

args = parser.parse_args()

print(sys.argv)
    
if args.append:
    append = args.append
else:
    append = None

if args.icsv:
    csv_file_loc = args.icsv
else:
    pass # raise Exception("Please insert raw data file location")

if args.oloc:
    file_loc = args.oloc
# else:
    # raise Error("Please insert excel file")

if args.ofile:
    output_file_name = args.ofile
    if not output_file_name.endswith('.xlsx'):
        output_file_name += '.xlsx'
else:
    if not append:
        output_file_name = [x for x in os.listdir(file_loc) if x.endswith(".xlsx")]
        
        if len(output_file_name) > 2:
           print("Please specify file name")
           raise Error("Please specify file name")
    
    
if args.ixl:
    input_excel_list = args.ixl.split(',')
    for input_excel in input_excel_list:
        if not input_excel.endswith('.xlsx'):
            input_excel += '.xlsx'
else:
    os.chdir(file_loc)
    input_excel_list = [x for x in os.listdir(file_loc) if x.endswith(".xlsx")]
    


args1, args2, args3 = args.args1, args.args2, args.args3



def read_Excel():
    df_list = []
    output_full_path = file_loc + "\\" + output_file_name[0]
    os.chdir(file_loc)
    
    if append:
        for file in input_excel_list:
            xls = pd.ExcelFile(file, engine="openpyxl")
            df = pd.read_excel(xls, 0)
            df_list.append(df)
        return df_list, output_full_path
    
    else:
        xls = pd.ExcelFile(output_full_path, engine="openpyxl")
        oldDF = pd.read_excel(xls, 0)
        oldDF = oldDF.set_index(args1)
    
        return oldDF, output_full_path



def read_append_csv(df):
    os.chdir(csv_file_loc)
    files = [x for x in os.listdir(csv_file_loc) if x.endswith(".csv")]
    if not files:
        print(f"File not found in the folder: {csv_file_loc} ...\nExitting!")
        sys.exit(1)

    resultDFList = [] #list
    for file in range(len(files)):
        os.chdir(csv_file_loc)
        print(f"Extracting data from [{files[file]}] ...")

        rawDF = pd.read_csv(files[file])
        resultDFList.append(rawDF)

        name = files[file].split(".csv")[0]
        resultName = "Result " + name
        percentName = name
        
        argslist = [args1, args2, args3]
        resultDFList[file] = resultDFList[file][argslist]
        resultDFList[file] = resultDFList[file].set_index(args1)
        resultDFList[file] = resultDFList[file].rename(columns={args2:resultName, args3:percentName})

    compileDF = pd.DataFrame()
    for file in range(len(files)):
        compileDF = compileDF.merge(resultDFList[file], left_index=True, right_index=True, how="outer", suffixes=('','_y'))

    df = df.merge(compileDF, left_index=True, right_index=True, how="outer", suffixes=('','_y'))
    df.sort_index(axis=1, inplace=True) # sort column
    df.sort_values(["Parent3","Parent2","Name"], ascending=True, inplace=True, na_position="first") # sort rows


    return df

def add_csv_to_excel():
    df, full_path = read_Excel()
    df = read_append_csv(df)
    return df, full_path


def compile_multi_excels():
    a=1
    df_list, full_path = read_Excel()
    iosf.create_excel_file(full_path)

    for df in df_list:
        name = "sheet" + str(a)
        iosf.append_to_sheet(df, full_path, name)
        a+=1


if __name__ == "__main__":
    
    if append:
        compile_multi_excels()
    else:
        df, output_full_path = add_csv_to_excel()
        excelWorkbook = load_workbook(output_full_path)
        writer = pd.ExcelWriter(output_full_path, engine='openpyxl')
        writer.book = excelWorkbook
        df.to_excel(writer, header=True)
        writer.save()
        
    print("Done...")