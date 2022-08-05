#-*- coding:<Shift> -*-
import networkx as nx
import numpy as np
import openpyxl
import pandas as pd
import glob as g
import re
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager
import math as m
import japanize_matplotlib

root = '../files/'
file = 'nikkei225_returns.csv'
# print([f.name for f in matplotlib.font_manager.fontManager.ttflist])

def node_coll(c):
    if c > 0:
        return "pink"
    else:
        return "cyan"

def node_col(c):
    if c == 1:
        return 'darkgreen'
    elif c == 2:
        return 'blue'
    elif c==3:
        return 'darkviolet'
    elif c==4:
        return 'indigo'
    elif c==5:
        return 'red'
    elif c==6:
        return 'black'
    
    return 'gray'

def main():
    df = pd.read_csv(root+file,encoding="UTF-8")
    df = df.set_axis(['code','mean','median','min','max','variance','brand'],axis=1)
    
    graph = nx.Graph()
    compval = 1
    data = df.values.tolist()
    print(df.describe())
    
    for i in range(len(data)):
        for j in range(i):
            brand1 = data[i][0]
            brand2 = data[j][0]
            value1 = data[i][compval]*100
            value2 = data[j][compval]*100
            
            val1 = 0
            val2 = 0
            if brand1 not in graph:
                if value1 > 0:
                    val1 = 1
                else:
                    val1 = -1
                
                graph.add_node(brand1,type='brand',value=val1)
                
            if brand2 not in graph:
                if value2 > 0:
                    val2 = 1
                else:
                    val2 = -1
                graph.add_node(brand2,type='brand',value=val2)
            
            if m.fabs(value1-value2) <= 0.000075 and not graph.has_edge(brand1,brand2):
                graph.add_edge(brand1,brand2,similar=1)
            elif m.fabs(value1-value2) <= 0.0001 and not graph.has_edge(brand1,brand2):
                graph.add_edge(brand1,brand2,similar=2)
            elif m.fabs(value1-value2) <= 0.0003 and not graph.has_edge(brand1,brand2):
                graph.add_edge(brand1,brand2,similar=3)
            elif m.fabs(value1-value2) <= 0.0005 and not graph.has_edge(brand1,brand2):
                graph.add_edge(brand1,brand2,similar=4)
            elif m.fabs(value1-value2) <= 0.00075 and not graph.has_edge(brand1,brand2):
                graph.add_edge(brand1,brand2,similar=5)
            elif m.fabs(value1-value2) <= 0.001 and not graph.has_edge(brand1,brand2):
                graph.add_edge(brand1,brand2,similar=6)
            else:
                pass
            # if value1 > soaring and value2 > soaring and not graph.has_edge(brand1,brand2):
            #     graph.add_edge(brand1,brand2)
            # elif value1 < crash and value2 < crash and not graph.has_edge(brand1,brand2):
            #     graph.add_edge(brand1,brand2)
            # elif (value1 <= soaring and value1 >= rise) and (value2 <= soaring and value2 >= rise) and not graph.has_edge(brand1,brand2):
            #     graph.add_edge(brand1,brand2)
            # elif (value1 >= crash and value1 <= drop) and (value2 >= crash and value2 <= drop) and not graph.has_edge(brand1,brand2):
            #     graph.add_edge(brand1,brand2)
            # elif (value1 >= 0 and value1 < rise) and (value2 >= 0 and value2 < rise) and not graph.has_edge(brand1,brand2):
            #     graph.add_edge(brand1,brand2)
            # elif (value1 <= 0 and value1 > drop) and (value2 <= 0 and value2 > drop) and not graph.has_edge(brand1,brand2):
            #     graph.add_edge(brand1,brand2)
            # else:
            #     pass
    # print(graph.number_of_nodes())
    plt.figure(figsize=(16,9))
    pos = nx.kamada_kawai_layout(graph)
    # print(graph.edges)
    nx.draw(
        graph,
        pos,
        node_size=200,
        node_color=[node_coll(graph.nodes[u]['value']) for u in graph.nodes],
        edge_color=[node_col(graph.edges[u]['similar']) for u in graph.edges],
        with_labels=True
    )

    name = ""
    if compval == 1:
        name="mean"
    elif compval == 2:
        name="median"
    elif compval == 3:
        name="min"
    elif compval == 4:
        name = "max"
    else:
        pass
    
    # return
    
    figname="nikkei225_nw_"+name+"v1.png"
    plt.savefig("../img/"+figname)
    plt.show()
        
    
    
if __name__ == "__main__":
    main()
    
    
