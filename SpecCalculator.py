import spec
from data_df_repos import *

gain = 0
offset = 0

df = pd.read_excel("C:\\Users\\weichan\\Downloads\\BalsaIssue\\LPQ2\\SlotTest\\testing.xlsx")
df_psup = keyword_filter_row(df, "Parent3", "PowerSupply")
df_load = keyword_filter_row(df, "Parent3", "ELoad")
# df_psup.append(df_load)
# ======================================================================
df_load_CR = keyword_filter_row(df_load, "Parent2", "Resistance")
df_load_CP = keyword_filter_row(df_load, "Parent2", "Power")
df_load_CC = keyword_filter_row(df_load, "Parent2", "CurrentAccuracy")
df_load_CV = keyword_filter_row(df_load, "Parent2", "Voltage")

df_psup_CC = keyword_filter_row(df_psup, "Parent2", "Current")
df_psup_CV = keyword_filter_row(df_psup, "Parent2", "Voltage")
# ======================================================================
df_load_CR_prog = keyword_filter_row(df_load_CR, "Name", "Prog")
df_load_CP_prog = keyword_filter_row(df_load_CP, "Name", "Prog")
df_load_CC_prog = keyword_filter_row(df_load_CC, "Name", "Prog")
df_load_CV_prog = keyword_filter_row(df_load_CV, "Name", "Prog")

df_load_CP_rdbk = keyword_filter_row(df_load_CP, "Name", "Rdbk")
df_load_CC_rdbk = keyword_filter_row(df_load_CC, "Name", "Rdbk")
df_load_CV_rdbk = keyword_filter_row(df_load_CV, "Name", "Rdbk")

df_psup_CC_prog = keyword_filter_row(df_psup_CC, "Name", "Prog")
df_psup_CV_prog = keyword_filter_row(df_psup_CV, "Name", "Prog")

df_psup_CC_rdbk = keyword_filter_row(df_psup_CC, "Name", "Rdbk")
df_psup_CV_rdbk = keyword_filter_row(df_psup_CV, "Name", "Rdbk")

df_string = df_psup_CV_prog.to_string()
print(df_string)
if all(map(df_string.__contains__, spec.PSUP_Voltage_Prog_High)):
    print("AAA")
else:
    print("f")
    