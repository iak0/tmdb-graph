
from d3blocks import D3Blocks
import pandas as pd
import pickle
from Q1 import Graph

SIZE_LOOKUP = {4: 30, 3: 20, 2: 10, 1:5}
COLOR_LOOKUP = {4: "#111111", 3: "#333333", 2:"#555555", 1:"#777777"}

def viz(graph):
    name_dict = {a: b for (a, b) in graph.nodes}
    named_edges = [(name_dict[a], name_dict[b], graph.edge_weights[(a,b)]) for (a, b) in graph.edges]

    d3 = D3Blocks()
    df = pd.DataFrame(named_edges, columns=("source", "target", "weight"))
    d3.d3graph(df)

    for node in graph.nodes:
        sanitized_name = node[1].replace(" ", "_")
        weight = graph.node_weights[node]
        if sanitized_name in d3.D3graph.node_properties:
            d3.D3graph.node_properties[sanitized_name]['size'] = SIZE_LOOKUP[weight]
            d3.D3graph.node_properties[sanitized_name]['label'] = node[1]
            d3.D3graph.node_properties[sanitized_name]['fontcolor'] = COLOR_LOOKUP[weight]
            d3.D3graph.node_properties[sanitized_name]['fontsize'] = SIZE_LOOKUP[weight]
    d3.D3graph.show(filepath="./index.html")

    
if __name__ == "__main__":
    with open('graph.txt', 'rb') as file:
        graph = pickle.load(file)
        viz(graph)