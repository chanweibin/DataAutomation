# [Balsa]
# ==================== LOAD PROG =========================================
load_V_High_prog = {
    "Gain"  :   0.0003,
    "Offset":   0.015
}
load_V_Low_prog = {
    "Gain"  :   0.0003,
    "Offset":   0.0042
}

load_C_High_prog = {
    "Gain"  :   0.0005,
    "Offset":   0.0072
}
load_C_Low_prog = {
    "Gain"  :   0.0005,
    "Offset":   0.00082
}

load_R_High_prog = {
    "Gain"  :   0.001,
    "Offset":   0.0018
}
load_R_Mid_prog = {
    "Gain"  :   0.001,
    "Offset":   0.016
}
load_R_Low_prog = {
    "Gain"  :   0.001,
    "Offset":   0.16
}

load_P_High_prog = {
    "Gain"  :   0.0008,
    "Offset":   1.5
}
load_P_Mid_prog = {
    "Gain"  :   0.0008,
    "Offset":   0.15
}
load_P_Low_prog = {
    "Gain"  :   0.0008,
    "Offset":   0.018
}

# ========================== LOAD RDBK =======================================
load_V_High_rdbk = load_V_High_prog
load_V_Low_rdbk = load_V_Low_prog

load_C_High_rdbk = load_C_High_prog
load_C_Low_rdbk = load_C_Low_prog
load_P_High_rdbk = load_P_High_prog
load_P_Mid_rdbk = load_P_Mid_prog
load_P_Low_rdbk = load_P_Low_prog
# ============================= PSUP PROG =======================================
psup_V_Auto_rdbk = {
    "Gain"  :   0.00025,
    "Offset":   0.0015
}

psup_C_High_rdbk = {
    "Gain"  :   0.0005,
    "Offset":   0.00025
}
psup_C_Mid_rdbk = {
    "Gain"  :   0.0003,
    "Offset":   0.0003
}
psup_C_Low_rdbk = {
    "Gain"  :   0.00035,
    "Offset":   0.00001
}

# ============================= PSUP prog =======================================

psup_V_Auto_prog = psup_V_Auto_rdbk

psup_C_High_prog = {
    "Gain"  :   0.0003,
    "Offset":   0.0008
}
psup_C_Mid_prog = psup_C_High_prog
psup_C_Low_prog = psup_C_High_prog

# ================================================================================


balsaSpec = {
    "PSUP"   :
    {
        "Current"   :
        {
            "Prog"  :
                {
                "High"  : psup_C_High_prog,
                "Low"   : psup_C_Low_prog
                },
            "Rdbk"  :
                {
                "High"  : psup_C_High_rdbk,
                "Low"   : psup_C_Low_rdbk
                },
                
        "Voltage":
        {
            "Prog"  :
                {    
                "Auto"  : psup_V_Auto_prog
                },
            "Rdbk"  :
                {
                "Auto"  : psup_V_Auto_rdbk
                }}}},
    "LOAD":
    {
        "Current":
        {
            "Prog"  :
                {
                    "High"  : load_C_High_prog,
                    "Low"   : load_C_Low_prog
                },
            "Rdbk"  :
                {
                    "High"  : load_C_High_rdbk,
                    "Low"   : load_C_Low_rdbk
                }
        },
        
        "Voltage":
        {
            "Prog"  :
                {
                    "High"  : load_V_High_prog,
                    "Low"   : load_V_Low_prog
                },
            "Rdbk"  :
                {
                    "High"  : load_V_High_rdbk,
                    "Low"   : load_V_Low_rdbk
                }
        },
        
        "Power":
        {
            "Prog"  :
                {
                    "High"  : load_P_High_prog,
                    "Mid"   : load_P_Mid_prog,
                    "Low"   : load_P_Low_prog
                },
            "Rdbk"  :
                {
                    "High"  : load_P_High_rdbk,
                    "Mid"   : load_P_Mid_rdbk,
                    "Low"   : load_P_Low_rdbk
                }
        },
        "Resistance":
        {
            "Prog"  :
                {
                    "High"  : load_R_High_prog,
                    "Mid"   : load_R_Mid_prog,
                    "Low"   : load_P_Low_prog
                }
        }
    }
}

balsaRange = {
    "PSUP"  :   
        {
        "Voltage"   : 
            {
            "Auto"  : ["Auto", "Range30V"]
            },
        "Current"   :
            {
            "High"  : ["Range20A", "High"],
            "Mid"   : ["Range2A", "Mid", "Medium"],
            "Low"   : ["Range0.11A", "Lo", "Low"]
            }
        },
    "LOAD"  :
        {
            "Voltage"   :
                {
                    "High"  :   ["Range60V", "High"],
                    "Low"   :   ["Range15V", "Low"]
                }
        }
        
}
            
        

x = balsaSpec["LOAD"]["Resistance"]["Prog"]["Low"]["Offset"]
print(x)

PSUP_Voltage_Prog_Low = ["PowerSupply", "Voltage", "Prog", "Low"]
PSUP_Voltage_Prog_High = ["PowerSupply", "Voltage", "Prog", "Range30V"]