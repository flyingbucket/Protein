import pandas as pd
import os
from datetime import datetime

edge_folder_path = r'G:\protein_in_G\data\csv'

edge_ls=os.listdir(edge_folder_path)
print(edge_ls)

# 将文件名去掉扩展名并转换为日期对象，然后进行排序
edge_ls_sorted = sorted(edge_ls, key=lambda x: datetime.strptime(x.replace('.csv', ''), '%Y-%m-%d'))
print(edge_ls_sorted)

i=2012
names=[]
sheets=[]
for file in edge_ls_sorted:
    i+=1
    name='y'+str(i)
    names.append(name)
    # print(file.replace('.csv', ''))
    globals()[name]=pd.read_csv(os.path.join(edge_folder_path, file), header=0)
    sheets.append(globals()[name])
    # print(globals()[name].head())

print(names)

# 创建一个 ExcelWriter 对象
with pd.ExcelWriter('output.xlsx') as writer:
    for i in range(len(names) - 1):
        print(names[i], names[i + 1])

        former = globals()[names[i]][['Protein A', 'Protein B', 'Score']].rename(columns={'Score': 'Score_old'})
        latter = globals()[names[i + 1]][['Protein A', 'Protein B', 'Score']].rename(columns={'Score': 'Score_new'})

        # 合并两个 DataFrame
        df_merged = pd.merge(former, latter, on=['Protein A', 'Protein B'], how='outer')

        # 将空缺的 score 填充为 0
        df_merged['Score_old'] = df_merged['Score_old'].fillna(0)
        df_merged['Score_new'] = df_merged['Score_new'].fillna(0)
        print(df_merged.head())

        # 计算Score增量
        df_merged['Score_diff'] = df_merged['Score_new'] - df_merged['Score_old']

        # 以Score_diff的绝对值进行降序排序
        df_merged = df_merged.sort_values(by='Score_diff', key=lambda x: x.abs(), ascending=False)
        print(df_merged.head())

        # 生成 sheet 名
        sheet_name = f"{edge_ls_sorted[i].replace('.csv','')} ~ {edge_ls_sorted[i + 1].replace('.csv','')}"
        
        # 将 df_merged.head() 写入 Excel 文件
        df_merged.head().to_excel(writer, sheet_name=sheet_name, index=False)
    print("\a")