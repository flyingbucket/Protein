import pandas as pd 


# 读取数据并转换为csv格式
data=pd.read_csv('D:\mypython\math_modeling\protein\data',sep=';',header=0)
data.to_csv('D:\mypython\math_modeling\protein\data.csv',index=False)