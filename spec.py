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
    "PowerSupply"   :
    {
        "CurrentAccuracy"   :
        {
            "Prog"  :
                {
                "20"  : psup_C_High_prog,
                "2"   : psup_C_Low_prog
                },
            "Rdbk"  :
                {
                "20"  : psup_C_High_rdbk,
                "2"   : psup_C_Low_rdbk
                },
        },
        "VoltageAccuracy":
        {
            "Prog"  :
                {    
                "30"  : psup_V_Auto_prog
                },
            "Rdbk"  :
                {
                "30"  : psup_V_Auto_rdbk
                }}},
    "ELoad":
    {
        "CurrentAccuracy":
        {
            "Prog"  :
                {
                    "40"  : load_C_High_prog,
                    "4"   : load_C_Low_prog
                },
            "Rdbk"  :
                {
                    "40"  : load_C_High_rdbk,
                    "4"   : load_C_Low_rdbk
                }
        },
        
        "VoltageAccuracy":
        {
            "Prog"  :
                {
                    "60"  : load_V_High_prog,
                    "15"   : load_V_Low_prog
                },
            "Rdbk"  :
                {
                    "60"  : load_V_High_rdbk,
                    "15"   : load_V_Low_rdbk
                }
        },
        
        "PowerAccuracy":
        {
            "Prog"  :
                {
                    "250"  : load_P_High_prog,
                    "25"   : load_P_Mid_prog,
                    "5"   : load_P_Low_prog
                },
            "Rdbk"  :
                {
                    "250"  : load_P_High_rdbk,
                    "25"   : load_P_Mid_rdbk,
                    "5"   : load_P_Low_rdbk
                }
        },
        "ResistanceAccuracy":
        {
            "Prog"  :
                {
                    "4000"  : load_R_High_prog,
                    "1250"   : load_R_Mid_prog,
                    "30"   : load_P_Low_prog
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
            

emul = "ELoad"
func = "ResistanceAccuracy"
type = "Prog"
Range = "1250"
Spec = "Gain"        

# x = eval("balsaSpec[emul]")
x = balsaSpec[emul][func][type][Range][Spec]
print(x)

# PSUP_Voltage_Prog_Low: list[str] = ["PowerSupply", "Voltage", "Prog", "Low"]
# PSUP_Voltage_Prog_High: list[str] = ["PowerSupply", "Voltage", "Prog", "Range30V"]