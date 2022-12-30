import networkx as nx
import pandas as pd
from .functionalities_34 import func_3


class ControllerGraph:
    def __init__(self, edges_df: pd.DataFrame):
        self.top_heroes = edges_df.groupby('hero').size().sort_values(ascending=False).index.tolist()

    def functionality(self, id, graph: nx.Graph, num_heroes: int = None, **kwargs):
        if num_heroes:
            try:  # This try and except clause allows us to understand the graph we are dealing with
                graph = graph.subgraph([x for x in graph.nodes if x in self.top_heroes[:num_heroes] or
                                        graph.nodes[x]['type'] == 'comic']) # Filter the heroes (not the comics)
            except KeyError:
                graph = graph.subgraph([x for x in graph.nodes if x in self.top_heroes[:num_heroes]])  # Filter heroes
        if id == 1:
            pass
        elif id == 2:
            pass
        elif id == 3:
            return func_3(graph, kwargs['seq'], kwargs['endpoints'])
        elif id == 4:
            pass
        elif id == 5:
            pass
        else:
            raise ValueError('There is no functionality for the chosen id.')
