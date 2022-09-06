import argparse, sys, os
import glob
import shutil
import pandas as pd
from openpyxl import Workbook, load_workbook
import data_df_repos as dfr
import io_read_file as iorf
import io_save_file as iosf
from datetime import datetime

# data file (txt) to dataframe
def read_datafile(inputfile_loc):
    df = pd.DataFrame({'Test Name':[],'Lo':[],'Result':[],'Hi':[],'%':[],'P/F':[]})

    file1 = open(inputfile_loc, 'r')
    Lines = file1.readlines()

    is_data = False
    for line in Lines:
        # indicate start of testpoints (reset df to get latest test)
        if "OUTPUT#" in line and "TESTS" in line:
            df = pd.DataFrame(columns=df.columns)
            is_data = True
            continue
        # indicate end of testpoints
        if "*** TEST RUN" in line:
            is_data = False
            continue
        # save line to dataframe if line is testpoint
        if is_data == True:
            # ignore lines with "Waveform for ..."
            if "Waveform for" in line or line == "":
                continue
            # split line by space
            data = line.split()
            # recombine testname if case it has space
            testname = data[0]
            for index in range(1,data.index(data[-6])+1):
                testname += " " + data[index]
            # Concatenate line into df
            new_row = pd.DataFrame({'Test Name':[testname],'Lo':[data[-5]],'Result':[data[-4]],'Hi':[data[-3]],'%':[data[-2]],'P/F':[data[-1]]})
            df = pd.concat([df,new_row],ignore_index=True)
    return df

def txt_file():
    # Read the first file
    current_file_loc = source + "\\" + files[0]
    df_temp = read_datafile(current_file_loc)
    df = pd.DataFrame()
    # Get the Test Name and % data only
    df['Test Name'] = df_temp['Test Name']
    df[files[0]] = df_temp['%']

    # Move first file to "Done" folder
    destination = source + "\\" + "Done"
    try:
        shutil.move(source + "\\" + files[0] , destination + "\\" + files[0])
    except FileNotFoundError:
        os.mkdir(destination)
        shutil.move(source + "\\" + files[0] , destination + "\\" + files[0])
    except:
        pass

    # Read every other files
    for file in range(1,len(files)):
        filename = files[file]
        current_file_loc = source + "\\" + filename
        df_temp = read_datafile(current_file_loc)
        # Merge the read with the main DF according to matching "Test Name"
        df = df.merge(df_temp[['Test Name','%']],on='Test Name',how='inner').drop_duplicates()
        df = df.rename(columns={'%':filename}) # Rename column header to filename

        # Move file to "Done" folder
        try:
            shutil.move(source + "\\" + filename , destination + "\\" + filename)
        except FileNotFoundError:
            os.mkdir(destination)
            shutil.move(source + "\\" + filename , destination + "\\" + filename)
        except:
            pass

    # Get list of all columns used to calculate mean and stdev
    cols = list(df.columns)
    cols.remove('Test Name')
    # Add Mean, Stdev, +3 Sigma, -3 Sigma
    df = dfr.derive_mean(df, cols)
    df = dfr.derive_std(df, cols)
    df['+3 Sigma'] = df['Mean'] + 3 * df['Stdev']
    df['-3 Sigma'] = df['Mean'] - 3 * df['Stdev']

    # Output to excel
    output_file_name = "3Sigma_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"
    output_full_name = input_file_loc + "\\3Sigma\\" + output_file_name
    iosf.dataframe_to_excel(df,output_full_name,"3Sigma")

def excel_file():
    # Read the first file
    current_file_loc = source + "\\" + files[0]
    xls = pd.ExcelFile(current_file_loc, engine="openpyxl")
    df_temp = pd.read_excel(xls,0,header=13,usecols="B,D")
    df = pd.DataFrame()
    # Get the Test Name and % data only
    df['Limit Name'] = df_temp['Limit Name']
    df[files[0]] = df_temp['Actual Value']

    # Move first file to "Done" folder
    destination = source + "\\" + "Done"
    try:
        shutil.move(source + "\\" + files[0] , destination + "\\" + files[0])
    except FileNotFoundError:
        os.mkdir(destination)
        shutil.move(source + "\\" + files[0] , destination + "\\" + files[0])
    except:
        pass

    # Read every other files
    for file in range(1,len(files)):
        filename = files[file]
        current_file_loc = source + "\\" + filename
        df_temp = pd.read_excel(xls,0,header=13,usecols="B,D")
        # Merge the read with the main DF according to matching "Test Name"
        df = df.merge(df_temp[['Limit Name','Actual Value']],on='Limit Name',how='inner')
        df.drop_duplicates(subset=['Limit Name'], keep='first', inplace=True, ignore_index=True)
        df = df.rename(columns={'Actual Value':filename}) # Rename column header to filename

        # Move file to "Done" folder
        try:
            shutil.move(source + "\\" + filename , destination + "\\" + filename)
        except FileNotFoundError:
            os.mkdir(destination)
            shutil.move(source + "\\" + filename , destination + "\\" + filename)
        except:
            pass

    # Get list of all columns used to calculate mean and stdev
    cols = list(df.columns)
    cols.remove('Limit Name')
    # Add Mean, Stdev, +3 Sigma, -3 Sigma
    df = dfr.derive_mean(df, cols)
    df = dfr.derive_std(df, cols)
    df['+3 Sigma'] = df['Mean'] + 3 * df['Stdev']
    df['-3 Sigma'] = df['Mean'] - 3 * df['Stdev']

    # Output to excel
    output_file_name = "3Sigma_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx"
    output_full_name = input_file_loc + "\\3Sigma\\" + output_file_name
    iosf.dataframe_to_excel(df,output_full_name,"3Sigma")

# MAIN
cwd = os.getcwd()
scriptName = sys.argv[0]
parser = argparse.ArgumentParser(description=str("Inputing arguments for " + scriptName))
parser.add_argument('-input', metavar="Input file location", help="Source file location", default=cwd)
args = parser.parse_args()

if args.input:
    input_file_loc = args.input

#input_file_loc = "C:\\Local_Storage\\3_Sigma"

# Look for files in Calc_3Sigma folder
source = input_file_loc + "\\Calc_3Sigma"
files = []
# Find every file that is not a folder and does not end with ".xlsx"
for item in os.listdir(source):
    if os.path.isfile(source + "\\" + item):
        files.append(item)

# End program if no files found
if not files:
    print(f"File not found in the folder: {input_file_loc} ...\nExitting!")
    sys.exit()

if (files[0].endswith(".xlsx")):
    excel_file()
else:
    txt_file()
