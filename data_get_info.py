import os
from random import random
import re
import sys
import math
import pandas as pd


#* ----------------------------------- Unit Info -----------------------------------
def get_unit_info(dfCol):
    
    try:
        
        firstRow = dfCol.first_valid_index()
        dut_info = dfCol.at[firstRow]
        
        
        dut_info = dut_info.split()
        serialNum = dut_info[-1]
        modelName = dut_info[-2]
        print("Serial Number: " + serialNum)
        print("Model Name: " + modelName)
        return serialNum, modelName

    except Exception as e:
        raise Exception("Error on getting SN/Model: " + e)




def get_SN(dfCol):
    try:
        sn, md = get_unit_info(dfCol)
        return sn
    except Exception as e:
        print("Error : " + e)
        sys.exit(1)




def get_model(dfCol):
    sn, md = get_unit_info(dfCol)
    return md



#* ----------------------------------- Test Info -----------------------------------

def get_PT_name():
    print("Feature not supported, currently PT is not included in output data ...")
    sys.exit(1)

def get_test_temp():
    pass


#* ----------------------------------- Indie PT Info -----------------------------------

# Power Supply 
def get_CV_info():
    
    return


def get_first_val(dfCol):
    firstRow = dfCol.first_valid_index()
    return dfCol.at[firstRow]
        
