import os, sys, re, argparse
import pandas as pd
from datetime import datetime

# IO file settings, currently not in use
user = 'weichan'
csv_file_loc = "C:\\Users\\{0}\\Downloads\\dataAutomation\\RAW_DATA\\".format(user)
output_file_loc = "C:\\Users\\{0}\\Downloads\\dataAutomation\\Output\\".format(user)
output_file_name = "outputfile-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"

# dataFrame settings
compiledResultDF = pd.DataFrame()

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

args = parser.parse_args()

if args.id and args.id.isdigit():
    id = int(args.id)
else:
    id = 0
    print("ID is null or non-digit, generating ID: {:04d}".format(id))

if args.csv:
    csv_file_loc = args.csv
else:
    pass#raise Exception("Please insert raw data file location")

if args.output:
    output_file_loc = args.output

if args.file:
    output_file_name = args.files
    if output_file_name.endswith('.xlsx'):
        pass
    else:
        output_file_name += '.xlsx'

if args.user:
    user = args.user

args1, args2, args3 = args.args1, args.args2, args.args3

def check_file_loc():

    try:
        if not os.path.exists(csv_file_loc):
            os.makedirs(csv_file_loc)
        if not os.path.exists(output_file_loc):
            os.makedirs(output_file_loc)

    except Exception as e:
        raise Exception(e)
        sys.exit(1)



def createDataFrame():

    try:
        resultDF = []

        files = [x for x in os.listdir() if ".csv" in x]
        if not os.listdir():
            print(f"File not found in the folder: {csv_file_loc} ...\nExitting!")
            sys.exit(1)

        print(files)
        for file in range(len(files)):
            print(f"Extracting data from {files[file]} ...")
            resultDF.append(pd.read_csv(files[file]))
            resultDF[file] = resultDF[file][[args1, args2, args3]]

            # workaround, ToDO: use regex to extract unit SN as ResultName
            resultName = args2 + str(file)
            percentName = args3 + str(file)
            resultDF[file] = resultDF[file].set_index(args1)
            resultDF[file] = resultDF[file].rename(columns={args2:resultName, args3:percentName})

        # compile df into single sheet
        compileDF = resultDF[0]
        for file in range(len(files)-1):
            compileDF = compileDF.join(resultDF[file+1])
        return compileDF

    except Exception as e:
        raise Exception(e)
        sys.exit(1)


if __name__ == '__main__':
    check_file_loc()
    compiledResultDF = createDataFrame()
    print(f"\nCompile data to {output_file_name} ... \n")
    writer = pd.ExcelWriter(output_file_name, engine='xlsxwriter')
    compiledResultDF.to_excel(writer, sheet_name="Sheet1", index=True, header=True)
    writer.save()
    sys.exit(0)
