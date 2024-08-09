import pickle
import networkx as nx

# 定义文件路径
graph_file_path = r'D:\mypython\math_modeling\protein\data\graph\all.pkl'

with open(graph_file_path, 'rb') as f:
    G = pickle.load(f)
print(G.number_of_nodes())
print(G.number_of_edges())
# 获取第一个节点的data字典的键
first_node = next(iter(G.nodes(data=True)))
_, data_dict1 = first_node
print(f"Data keys in each node: {list(data_dict1.keys())}")

frist_edge = next(iter(G.edges(data=True)))
_,_, data_dict2 = frist_edge 
print(f"Data keys in each node: {list(data_dict2.keys())}")