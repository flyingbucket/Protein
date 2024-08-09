import os
import pandas as pd
import networkx as nx
import pickle
from multiprocessing import Pool

# 定义结果文件路径
result_file =r'D:\mypython\math_modeling\protein\result\Q3DC.xlsx'
# 定义文件夹路径
csv_folder_path = r'D:\mypython\math_modeling\protein\data\csv'
graph_folder_path = r'D:\mypython\math_modeling\protein\data\graph'

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
    degree_centrality = nx.degree_centrality(G)
    
    # 将结果存储到DataFrame中
    result_df = pd.DataFrame(list(degree_centrality.items()), columns=['Node', 'Degree_Centrality'])
    
    return filename, result_df

def main():
    # 获取所有CSV文件
    csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
    
    # 排除最后一个文件
    if csv_files:
        csv_files = csv_files[:-1]

    # 使用多进程处理文件
    with Pool() as pool:
        results = pool.map(process_file, csv_files)
    
    # 按照文件名中的数字升序排列
    results.sort(key=lambda x: int(''.join(filter(str.isdigit, x[0]))))
    
    # 将结果写入Excel文件的不同Sheet中
    with pd.ExcelWriter(result_file) as writer:
        for filename, result_df in results:
            sheet_name = os.path.splitext(filename)[0]
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == '__main__':
    main()
    # A,B=process_file('all.csv')