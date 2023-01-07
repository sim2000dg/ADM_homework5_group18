import networkx as nx


# This functionality produces the value of one of the possible metrics that the user can choose from
# Betweeness Centrality, Page Rank, #Closeness Centrality and Degree Centrality; calculated on the entire graph or on
# a subgraph made up of the N nodes (the number N is also #chosen by the user) that represent the heroes appearing in
# the most number of comics. It produces also the value of the chosen metric #calculated on a specific hero
# (also chosen by the user)

def func2(graph, hero, metric):
    # We calculate the metric for the entire graph
    if metric == 'betweenness_centrality':
        metric_values = nx.betweenness_centrality(graph)  # if the user chooses the betweenness centrality metric
    elif metric == 'pagerank':
        metric_values = nx.pagerank_numpy(graph)  # if the user chooses the pagerank metric
    elif metric == 'closeness_centrality':
        metric_values = nx.closeness_centrality(graph)  # if the user chooses the closeness centrality metric
    elif metric == 'degree_centrality':
        metric_values = nx.degree_centrality(graph)  # if the user chooses the degree centrality metric
    else:
        raise ValueError('Invalid metric')
    
    # We calculate the metric for the given hero
    hero_metric_value = metric_values[hero]
    
    return metric_values, hero_metric_value

    
