from msilib.schema import Error
import pandas as pd
import argparse, os, sys
from openpyxl import load_workbook

output_file_loc = os.getcwd()
csv_file_loc = os.getcwd()


parser = argparse.ArgumentParser(description="This script helps to append csv file(s) into compiled excel sheet")
parser.add_argument('-csv', metavar="CSV", help="CSV files folder location")
parser.add_argument('-output', metavar="Output file location", help="Location of file data to add in")
parser.add_argument('-file', metavar="Output file name")
parser.add_argument('-args1', metavar="Column1 Name", default="Name")
parser.add_argument('-args2', metavar="Column2 Name", default="Result")
parser.add_argument('-args3', metavar="Column3 Name", default="PercentSpec")

args = parser.parse_args()

if args.csv:
    csv_file_loc = args.csv
else:
    pass # raise Exception("Please insert raw data file location")

if args.output:
    output_file_loc = args.output
# else:
    # raise Error("Please insert excel file")

if args.file:
    output_file_name = args.file
    if not output_file_name.endswith('.xlsx'):
        output_file_name += '.xlsx'

args1, args2, args3 = args.args1, args.args2, args.args3



def read_Excel():
    
    os.chdir(output_file_loc)
    output_file_name = [x for x in os.listdir(output_file_loc) if x.endswith(".xlsx")]
    if len(output_file_name) > 2:
        raise Error("Nope")
    output_full_path = output_file_loc + "\\" + output_file_name[0]#.split('.xlsx')[0]
    xls = pd.ExcelFile(output_full_path, engine="openpyxl")
    oldDF = pd.read_excel(xls, 0)
    oldDF = oldDF.set_index(args1)
    
    # oldDF = pd.read_excel(output_file_name, engine="openpyxl")
    
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
        resultName = "raw " + name
        percentName = name
        
        argslist = [args1, args2, args3]
        resultDFList[file] = resultDFList[file][argslist]
        resultDFList[file] = resultDFList[file].set_index(args1)
        resultDFList[file] = resultDFList[file].rename(columns={args2:resultName, args3:percentName})

        compileDF = pd.DataFrame()
        for file in range(len(files)):
            compileDF = compileDF.merge(resultDFList[file], left_index=True, right_index=True, how="outer", suffixes=('','_y'))

    df = df.merge(compileDF, left_index=True, right_index=True, how="outer", suffixes=('','_y'))
    sortCols = df.columns.tolist()
    sortCols.sort()
    df = df[sortCols]

    return df

def add_csv_to_excel():
    df, full_path = read_Excel()
    df = read_append_csv(df)
    return df, full_path



if __name__ == "__main__":

    df, output_full_path = add_csv_to_excel()
    excelWorkbook = load_workbook(output_full_path)
    writer = pd.ExcelWriter(output_full_path, engine='openpyxl')
    writer.book = excelWorkbook
    df.to_excel(writer, header=True)
    writer.save()