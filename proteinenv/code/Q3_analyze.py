import os
import pandas as pd
import networkx as nx
import pickle
import multiprocessing
from datetime import datetime as dt
from multiprocessing import Pool


'''图中每条边代表一个研究数据,故节点度的变化可以反映一个蛋白质的研究热度'''
# 定义结果文件路径
result_file =r'J:\protein_in_ G\result\Q3DC.xlsx'
# 定义文件夹路径
csv_folder_path = r'J:\protein_in_ G\data\csv'
graph_folder_path = r'J:\protein_in_ G\data\graph'

def process_file(filename):
    file_path = os.path.join(csv_folder_path, filename)
    graph_file_path = os.path.join(graph_folder_path, filename.replace('.csv', '.pkl'))
    # 读取CSV文件
    df = pd.read_csv(file_path)
    
    # 创建图
    G = nx.Graph()
    for index, row in df.iterrows():
        weight = float(row['Score'])
        protein_a = row['Protein A']
        protein_b = row['Protein B']
        
        G.add_edge(protein_a,protein_b,weight=weight)

        G.nodes[protein_a]['gene']=row['Gene A']
        G.nodes[protein_b]['gene']=row['Gene B']
        G.nodes[protein_a]['Taxon']=row['Taxon A']
        G.nodes[protein_b]['Taxon']=row['Taxon B']
    
    with open(graph_file_path, 'wb') as f:
        pickle.dump(G, f)
    # 计算度中心性值
    degree_dict= dict(nx.degree(G)
    )    
    # 将结果存储到DataFrame中
    result_df = pd.DataFrame(list(degree_dict.items()), columns=['Node', 'Degree'])
    
    return filename, result_df

def parse_date_from_filename(filename):
    try:
        # 假设文件名格式为 'YYYY-MM-DD.csv'
        date_str = filename.split('.')[0]
        return dt.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print(f"Warning: Unable to parse date from filename {filename}")
        return dt.max  # 返回一个最大日期作为默认值


def main():
    # 获取所有CSV文件
    csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
    
    # 使用多进程处理文件
    with Pool() as pool:
        results = pool.map(process_file, csv_files)
    
    # 按照文件名中的数字升序排列
    results.sort(key=lambda x: parse_date_from_filename(x[0]))
    
    # 将结果写入Excel文件的不同Sheet中
    with pd.ExcelWriter(result_file) as writer:
        for filename, result_df in results:
            sheet_name = os.path.splitext(filename)[0]
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == '__main__':
    
    multiprocessing.freeze_support()
    main()
    # A,B=process_file('2013-04-10.csv')