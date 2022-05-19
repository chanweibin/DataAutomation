import argparse
import sys
import os
import re

# property
csv_file_loc = "C:\Users\weichan\Downloads\dataAutomation\RAW_DATA\\"
output_file_loc = "C:\Users\weichan\Downloads\dataAutomation\Output\\"
output_file_name = ""

scriptName = sys.argv[0]
parser = argparse.ArgumentParser(description=str("Inputing arguments for " + scriptName))
parser.add_argument('-id', metavar="ID", help="Key in four digit ID")
parser.add_argument('-csv', metavar="CSV", help="CSV file location")
parser.add_argument('-output', metavar="Target file location", help="Location of file data to add in")

args = parser.parse_args()


if args.id and args.id.isdigit():
    id = int(args.id)
else:
    id = 0
    print("ID is null or non-digit, generating ID: {:04d}".format(id))

if args.csv:
    csv_file_loc = args.csv
else:
    raise Exception("Please insert raw data file location")

if args.target:
    output_file_loc = args.target


print("{:04d}".format(id))

class PtFullResult:
    def __init__ (self, result1, result2):
        self.res1 = result1
        self.res2 = result2



class ptHalf(PtFullResult):
    def __init__ (self, result1, result2):
        super().__init__(result1, result2)
