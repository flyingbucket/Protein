import pandas as pd
import networkx as nx
from concurrent.futures import ProcessPoolExecutor
import sys
import pickle 

# 指定路径
data_path = r'I:\AAA\protein\data.csv'
graph_path = r'I:\AAA\protein\all.pkl'
output_path = r'I:\AAA\protein\top_100_nodes_per_subgraph.xlsx'
# 读取数据
data_df = pd.read_csv(data_path, header=0)


# 创建图
G = nx.Graph()
for index, row in data_df.iterrows():
    weight = float(row['Score'])
    protein_a = row['Protein A']
    protein_b = row['Protein B']
    
    G.add_edge(protein_a,protein_b,weight=weight)

    G.nodes[protein_a['gene']]=row['Gene A']
    G.nodes[protein_b['gene']]=row['Gene B']
    G.nodes[protein_a['Taxon']]=row['Taxon A']
    G.nodes[protein_b['Taxon']]=row['Taxon B']
print(G.number_of_nodes())
print(G.number_of_edges())

# 保存图
with open(graph_path, 'wb') as f:
    pickle.dump(G, f)

# 获取所有连通分量
subgraphs = [G.subgraph(c).copy() for c in nx.connected_components(G)]
print('共有{}个连通分量'.format(len(subgraphs)))

# 筛选出节点数量最多的十个子图
subgraphs_sorted = sorted(subgraphs, key=lambda sg: sg.number_of_nodes(), reverse=True)
top_10_subgraphs = subgraphs_sorted[:10]


# 计算特征向量中心性
def compute_eigenvector_centrality(subgraph):
    try:
        return nx.eigenvector_centrality(subgraph, weight='weight', max_iter=1500)  # 增加最大迭代次数
    except nx.exception.PowerIterationFailedConvergence as e:
        print(f"Failed to converge for subgraph: {e}")
        return {}  # 返回一个空字典表示未能计算出结果

if __name__ == '__main__':
    
    sys.setrecursionlimit(1500)  # 增加递归深度，防止内存溢出
    # 使用多进程计算每个子图的特征向量中心性
    with ProcessPoolExecutor() as executor:
        eigenvector_centralities = list(executor.map(compute_eigenvector_centrality, top_10_subgraphs))

    # 找出每个子图在特征向量中心性下的前100名
    def get_top_100_centrality_nodes(centrality_dict):
        return sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:100]

    top_100_nodes_per_subgraph = [get_top_100_centrality_nodes(ec) for ec in eigenvector_centralities]

    # 将每个子图的top_100_nodes_per_subgraph存储到一个Excel中
    with pd.ExcelWriter(output_path) as writer:
        for i, top_100_nodes in enumerate(top_100_nodes_per_subgraph, 1):
            df = pd.DataFrame(top_100_nodes, columns=['Node', 'Centrality'])
            df.to_excel(writer, sheet_name=f'Subgraph_{i}', index=False)

    print("数据已成功存储到top_100_nodes_per_subgraph.xlsx中")