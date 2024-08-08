import networkx as nx
import pandas as pd


# 读取数据
data_df=pd.read_csv('D:\mypython\math_modeling\protein\data.csv',header=0)
# print(data_df.columns)
edges=data_df[['Protein A','Protein B','Score']]

# 创建图
G=nx.Graph()
for index,row in edges.iterrows():
    G.add_edge(row['Protein A'],row['Protein B'],weight=row['Score'])

print(G.number_of_nodes())
print(G.number_of_edges())

# 计算中心性
degree_centrality=nx.degree_centrality(G)
closeness_centrality=nx.closeness_centrality(G,distance='weight')
betweenness_centrality=nx.betweenness_centrality(G,weight='weight')
eigenvector_centrality=nx.eigenvector_centrality(G,weight='weight')

def sort_dict(dict,n):
    return sorted(dict.items(),key=lambda x:x[1],reverse=True)[:n]

top_5_degree=sort_dict(degree_centrality,5)
top_5_closeness=sort_dict(closeness_centrality,5)
top_5_betweenness=sort_dict(betweenness_centrality,5)
top_5_eigenvector=sort_dict(eigenvector_centrality,5)

print('度中心性:',top_5_degree)
print('接近中心性:',top_5_closeness)
print('介数中心性:',top_5_betweenness)
print('特征向量中心性:',top_5_eigenvector)
