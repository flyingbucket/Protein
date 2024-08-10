import pandas as pd
import numpy as np


'''选出节点度变化的前五名'''

diff_path=r'G:\protein_in_G\result\node_diff.xlsx'
diff_dict=pd.read_excel(diff_path,sheet_name=None,header=0)

for sheet_name,df in diff_dict.items():
    df.sort_values(by='diff',ascending=True,inplace=True) #ascending=False 降序,ascending=True 升序,各跑一遍
    top5=df.head(5)
    print(sheet_name)
    print(top5[['Node','diff']])