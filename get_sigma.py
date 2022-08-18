import argparse, sys, os
import glob
import shutil
import pandas as pd
from openpyxl import Workbook, load_workbook
import data_df_repos as dfr
import io_save_file as iosf
from datetime import datetime

def read_datafile(inputfile_loc):
    # df = pd.read_fwf("C:\\Users\\weipong8\\Downloads\\OLYFTS8 12A\\C12002770.8")
    df = pd.DataFrame({'Test Name':[],'Lo':[],'Result':[],'Hi':[],'%':[],'P/F':[]})

    file1 = open(inputfile_loc, 'r')
    Lines = file1.readlines()

    is_data = False
    for line in Lines:
        if "OUTPUT#" in line and "TESTS" in line:
            df = pd.DataFrame(columns=df.columns)
            is_data = True
            continue
        if "*** TEST RUN" in line:
            is_data = False
            continue
        if is_data == True:
            test = line
            if "Waveform for" in line or line == "":
                continue
            data = line.split()
            testname = data[0]
            for index in range(1,data.index(data[-6])+1):
                testname += " " + data[index]
            new_row = pd.DataFrame({'Test Name':[testname],'Lo':[data[-5]],'Result':[data[-4]],'Hi':[data[-3]],'%':[data[-2]],'P/F':[data[-1]]})
            df = pd.concat([df,new_row],ignore_index=True)
    return df

# df = read_datafile('C:\\Users\\weipong8\\Downloads\\OLYFTS8 12A\\C12002770.8')

# input_file_loc = "C:\\Users\\weipong8\\Downloads\\OLYFTS8 12B"
scriptName = sys.argv[0]
parser = argparse.ArgumentParser(description=str("Inputing arguments for " + scriptName))
parser.add_argument('-input', metavar="Input file location", help="Source file location", default="E:\\6_Sigma") # input_file_loc = os.getcwd() + "\\"
args = parser.parse_args()

if args.input:
    input_file_loc = args.input

source = input_file_loc + "\\Calc_6Sigma"
files = []
for item in os.listdir(source):
    if os.path.isfile(source + "\\" + item) and not item.endswith(".xlsx"):
        files.append(item)

if not files:
    print(f"File not found in the folder: {input_file_loc} ...\nExitting!")
    sys.exit()

current_file_loc = source + "\\" + files[0]
df_temp = read_datafile(current_file_loc)
df = pd.DataFrame()
df['Test Name'] = df_temp['Test Name']
df[files[0]] = df_temp['%']

destination = source + "\\" + "Done"
try:
    shutil.move(source + "\\" + files[0] , destination + "\\" + files[0])
except FileNotFoundError:
    os.mkdir(destination)
    shutil.move(source + "\\" + files[0] , destination + "\\" + files[0])
except:
    pass

for file in range(1,len(files)):
    filename = files[file]
    current_file_loc = source + "\\" + filename
    df_temp = read_datafile(current_file_loc)
    # pd.set_option("display.max_rows",None,"display.max_columns",None)
    # print(df_temp[['Test Name','%']])
    df = df.merge(df_temp[['Test Name','%']],on='Test Name',how='inner').drop_duplicates()
    df = df.rename(columns={'%':filename})
    # print(df)
    try:
        shutil.move(source + "\\" + filename , destination + "\\" + filename)
    except FileNotFoundError:
        os.mkdir(destination)
        shutil.move(source + "\\" + filename , destination + "\\" + filename)
    except:
        pass

cols = list(df.columns)
cols.remove('Test Name')
df = dfr.derive_mean(df, cols)
df = dfr.derive_std(df, cols)
df['+3 Sigma'] = df['Mean'] + 3 * df['Stdev']
df['-3 Sigma'] = df['Mean'] - 3 * df['Stdev']

output_file_name = "6Sigma_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"
output_full_name = input_file_loc + "\\6Sigma\\" + output_file_name
iosf.dataframe_to_excel(df,output_full_name,"6Sigma")
