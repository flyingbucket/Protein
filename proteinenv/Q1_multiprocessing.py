import pandas as pd
import networkx as nx
from concurrent.futures import ProcessPoolExecutor

# 读取数据
data_df = pd.read_csv('D:\mypython\math_modeling\protein\data.csv', header=0)
edges = data_df[['Protein A', 'Protein B', 'Score']]

# 创建图
G = nx.Graph()
for index, row in edges.iterrows():
    weight = float(row['Score'])
    G.add_edge(row['Protein A'], row['Protein B'], weight=weight)

print(G.number_of_nodes())
print(G.number_of_edges())

# 获取所有连通分量
subgraphs = [G.subgraph(c).copy() for c in nx.connected_components(G)]
print('共有{}个连通分量'.format(len(subgraphs)))

# 筛选出节点数量最多的十个子图
subgraphs_sorted = sorted(subgraphs, key=lambda sg: sg.number_of_nodes(), reverse=True)
top_10_subgraphs = subgraphs_sorted[:10]


# 计算特征向量中心性
def compute_eigenvector_centrality(subgraph):
    return nx.eigenvector_centrality(subgraph, weight='weight')

# 使用多进程计算每个子图的特征向量中心性
with ProcessPoolExecutor() as executor:
    eigenvector_centralities = list(executor.map(compute_eigenvector_centrality, top_10_subgraphs))

# 找出每个子图在特征向量中心性下的前100名
def get_top_100_centrality_nodes(centrality_dict):
    return sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:100]

top_100_nodes_per_subgraph = [get_top_100_centrality_nodes(ec) for ec in eigenvector_centralities]

# 将每个子图的top_100_nodes_per_subgraph存储到一个Excel中
with pd.ExcelWriter(r'D:\mypython\math_modeling\protein\top_100_nodes_per_subgraph.xlsx') as writer:
    for i, top_100_nodes in enumerate(top_100_nodes_per_subgraph, 1):
        df = pd.DataFrame(top_100_nodes, columns=['Node', 'Centrality'])
        df.to_excel(writer, sheet_name=f'Subgraph_{i}', index=False)

print("数据已成功存储到top_100_nodes_per_subgraph.xlsx中")