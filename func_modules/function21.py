import networkx as nx
import pandas as pd
from collections import Counter


def func1(graph: nx.Graph, graph_type: int):
    """
    This function is created to extract the graph's features as:
    - The number of nodes in the network (if type 2, report for both node types)
    - The number of collaborations of each superhero with the others (only if type 1)
    - The number of heroes that have appeared in each comic (only if type 2) The network's density
    - The network's degree distribution
    - The average degree of the network
    - The network's Hubs (hubs are nodes having degrees more extensive than the 95th percentile of the degree distribution)
    - Whether the Network is sparse or dense
    """
    if not isinstance(graph_type, int):
        raise TypeError('You need to pass an integer to the function as graph type (1 or 2)')
    elif graph_type != 1 and graph_type != 2:
        raise ValueError('You need to pass 1 or 2 as integers for graph type')

    # hero_graph
    if graph_type == 1:
        # 1.The number of nodes in the network (if type 2, report for both node types)
        number_of_nodes = graph.number_of_nodes()  # using the built-in function from networkx

        # 2.The number of collaborations of each superhero with the others (only if type 1)
        edges = graph.edges
        number_of_collaborations = Counter()
        for i in edges:
            number_of_collaborations[i[0]] += 1

        # 3.The number of heroes that have appeared in each comic (only if type 2)
        heroes_in_comic = None

        # 4.The network's density
        density = nx.density(graph)  # using the built-in function from networkx

        # 5.The network's degree distribution
        networks_degree_distribution = nx.degree_histogram(graph)

        # 6.The average degree of the network
        # We simply use the built in function from networkx that create a dictionary
        # This function give the degree for each node
        # After that we take the mean
        average_degree = sum(dict(nx.degree(graph)).values()) / len(graph.nodes)

        # 7.The network's Hubs (hubs are nodes having degrees more extensive than the 95th
        # percentile of the degree distribution)

        # dictionary of the degrees for each node
        data = dict(nx.degree(graph))

        # put the dictionary into a dataframe, so we can use pandas built-in functions
        df_degree = pd.DataFrame.from_dict(data, orient='index', columns=['degree'])

        # take the values equal or above 95%
        network_hubs = df_degree[df_degree.degree >= df_degree.degree.quantile(0.95)].index

        # 8.Whether the Network is sparse or dense
        if density * 100 >= 10:
            network = "Dense"
        else:
            network = "Sparse"

    # hero_comics_graph
    elif graph_type == 2:
        # 1.The number of nodes in the network (if type 2, report for both node types)
        number_of_nodes = graph.number_of_nodes()  # using the built-in function from networkx

        # 2.The number of collaborations of each superhero with the others (only if type 1)
        number_of_collaborations = None

        # 3.The number of heroes that have appeared in each comic (only if type 2)
        heroes_in_comic = dict(
            [(x, graph.degree[x]) for x in graph.nodes if graph.nodes[x]['type'] == 'comic'])

        # 4.The network's density
        density = nx.density(graph)  # using the built-in function from networkx

        # 5.The network's degree distribution
        # Store the data for the plot
        networks_degree_distribution = nx.degree_histogram(graph)

        # 6.The average degree of the network
        # We simply use the built in function from networkx that create a dictionary.
        # This function give the degree for each node.
        # After that we take the mean.
        average_degree = sum(dict(nx.degree(graph)).values()) / len(graph.nodes)

        # 7.The network's Hubs (hubs are nodes having degrees more extensive than the 95th
        # percentile of the degree distribution)

        # put the dictionary heroes_in_comic into a dataframe, so we can use pandas built-in functions
        df_degree = pd.DataFrame.from_dict(heroes_in_comic, orient='index', columns=['degree'])

        # take the values equal or above 95%
        network_hubs = df_degree[df_degree.degree >= df_degree.degree.quantile(0.95)].index

        # 8.Whether the Network is sparse or dense
        if density * 100 >= 10:
            network = "Dense"
        else:
            network = "Sparse"

    return number_of_nodes, number_of_collaborations, heroes_in_comic, density, networks_degree_distribution, \
        average_degree, network_hubs, network
