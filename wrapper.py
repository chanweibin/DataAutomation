import argparse
import os 
import sys
import pandas as pd

from datetime import datetime
from openpyxl import load_workbook

# * File name and Location settings
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
