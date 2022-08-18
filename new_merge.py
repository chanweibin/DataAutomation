import pandas as pd
import io_save_file as iosf

df1 = pd.read_csv("C:\Local_Storage\Merge\\59.csv")

df2 = pd.read_csv("C:\Local_Storage\Merge\\E36731A_MY62100041_2022-08-06 10-35-10-Fail Correlation.csv")

df1 = df1[['LowerLimit','Result','UpperLimit','PercentSpec','Name']]

df2 = df2.drop(columns=['LowerLimit','Result','UpperLimit','PercentSpec','Guid','Status'])

df = df1.merge(df2,on='Name')

pd.set_option("display.max_rows",None,"display.max_columns",None)
print(df)

iosf.dataframe_to_excel(df,"C:\Local_Storage\Merge\\59.xlsx")