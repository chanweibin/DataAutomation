import os
from random import random
import re
import sys
import math
import numpy as np 



def get_unit_info(dfCol):
    
    try:
        dut_info = None
        dfCol.fillna(0, inplace=True)
        print(dfCol)

        cnt = 0
        while (dut_info is None) or (dut_info == 0) :
            dut_info = dfCol[cnt]
            cnt+=1
        
        dut_info = dut_info.split()
        serialNum = dut_info[-1]
        modelName = dut_info[-2]
        print("Serial Number: " + serialNum)
        print("Model Name: " + modelName)

        return serialNum, modelName

    except Exception as e:
        raise Exception(e)




def get_SN(dfCol):
    sn, md = get_unit_info(dfCol)
    return sn




def get_model(dfCol):
    sn, md = get_unit_info(dfCol)
    return md





def get_PT_name():
    print("Feature not supported, currently PT is not included in output data ...")
    sys.exit(1)

def get_test_temp():
    pass
