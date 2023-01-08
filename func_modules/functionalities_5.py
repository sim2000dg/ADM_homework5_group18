import networkx as nx
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math


def func_5(graph: nx.Graph, hero1=None, hero2=None):
    graph1 = nx.Graph(graph)  # copy original graph
    num = nx.number_connected_components(graph1)  # count connected components
    num1 = num
    dictbet = nx.edge_betweenness_centrality(graph1, weight='weight')  # calculate edge betweenness centrality
    # for each edges
    sort = sorted(dictbet.items(), key=lambda kv: kv[1])  # sort the edges by edge betweenness centrality
    sort = [i[0] for i in sort]  # from dict to list

    while (num1 == num):  # until the number of connected components doesn't increase
        graph1.remove_edge(sort[0][0], sort[0][1])  # remove the edges with highest edge betweenness centrality
        sort.remove(sort[0])
        num1 = nx.number_connected_components(graph1)  # calculate the number connected components

    numedges = graph.number_of_edges() - graph1.number_of_edges()  # initial edges - final edges

    checkhero = False
    for i in nx.connected_components(graph1):  # check if there is a community which
        if ((hero1 in i) and (hero2 in i)):  # contain both the heros
            checkhero = True

    return numedges, graph1, checkhero, graph


def root(num, r):  # function which finds the r-th roots given num
    base = num ** (1.0 / r)  # (we use this to divide the communities in the plot)
    roots = []
    for i in range(0, r):
        radice = complex(base * math.cos(2 * math.pi * i / r), base * math.sin(2 * math.pi * i / r))
        roots.append(np.array([np.real(radice), np.imag(radice)]))
    return roots


def faitabella(G, comps):  # function which creates the table
    dictcomps = {}
    for num, i in enumerate(comps):
        a = 'Group ' + str(num)
        dictcomps[a] = i
    print(tabulate(dictcomps, headers='keys'))


def colorgraph(G, comps):  # function which defines nodes' color and position by belonging community

    pos = nx.spring_layout(G)  # start with position = spring_layout
    color_map = dict.fromkeys(G)
    numcomps = len(comps)
    radalto = root(1, numcomps)  # calculate 'numcomps' roots of 1
    for node in G:
        j = 0
        while not (node in comps[j]):  # if the node belongs to the j-th component, traslate its position
            j += 1  # move it j-th root of one
        pos[node] += 0.5 * radalto[j - 1]
        color_map[node] = j  # give 'j' as a 'color'

    return color_map, pos


def identifygroup(G, h1, h2, color_map):
    """
    function which plot graph and color communities, specify the hero1 and hero2 communities
    (eventually the same):

    * G: nx.graph() 
    * h1, h2: str()
    * color_map: dict(), keys = heros, values = color
    """

    colorh = []
    for i in color_map:
        if color_map[i] == color_map[h1]:  # all the heros in the hero1's community
            colorh.append('red')  # are 'red'
        elif color_map[i] == color_map[h2]:  # all the heros in the hero2's community 
            colorh.append('green')  # are 'green'
        else:
            colorh.append('blue')  # the other are blue

    name = dict.fromkeys(G, '')
    name[h1] = h1
    name[h2] = h2

    bordcol = []
    for num, i in enumerate(color_map):  # color black the edges of hero1, hero2 nodes
        if i in [h1, h2]:
            bordcol.append('black')
        else:
            bordcol.append(colorh[num])

    # build patches and create the legend
    if color_map[h1] != color_map[h2]:
        if 'blue' in color_map.values():
            h1_patch = mpatches.Patch(color='red', label=h1)
            h2_patch = mpatches.Patch(color='green', label=h2)
            altro_patch = mpatches.Patch(color='blue', label='All the others')
            plt.legend(handles=[h1_patch, h2_patch, altro_patch])
        else:
            h1_patch = mpatches.Patch(color='red', label=h1)
            h2_patch = mpatches.Patch(color='green', label=h2)
    else:
        h1_patch = mpatches.Patch(color='red', label=h1 + ' \\ ' + h2)
        altro_patch = mpatches.Patch(color='blue', label='All the others')
        plt.legend(handles=[h1_patch, altro_patch])

    # plot the graph
    nx.draw(G, node_color=colorh, with_labels=True, labels=name, edgecolors=bordcol)
    plt.margins(x=0.10)
    plt.show()

    return None
