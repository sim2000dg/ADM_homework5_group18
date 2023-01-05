import networkx as nx
import pandas as pd
from .functionalities_34 import func_3, func_4


class ControllerGraph:
    """
    The aim of this class is to act as a controller for the requested functionalities. Once initialized, the object also
    holds the list of the top n heroes, which is then used by the functionalities (if needed) to work on subgraphs.

    The `functionality` method is the core of the class, allowing to call each of the five class in a compact and
    consistent way.
    """
    def __init__(self, edges_df: pd.DataFrame) -> None:
        self.top_heroes = edges_df.groupby('hero').size().sort_values(ascending=False).index.tolist()

    def functionality(self, id, graph: nx.Graph, num_heroes: int = None, **kwargs):
        """
        This method acts as an interface to the functionalities.
        :param id: The id of the requested functionality.
        :param graph: The graph to use for the functionalities.
        :param num_heroes: The number of top heroes to consider to build a subgraph to work on. If not passed, the
            functionalities work on the complete graph.
        :param kwargs: Additional keyword arguments which are then passed to the specific functionalities.
        :return:
        """
        if num_heroes:
            try:  # This try and except clause allows us to understand the graph we are dealing with
                graph = graph.subgraph([x for x in graph.nodes if x in self.top_heroes[:num_heroes] or
                                        graph.nodes[x]['type'] == 'comic'])  # Filter the heroes (not the comics)
            except KeyError:
                graph = graph.subgraph([x for x in graph.nodes if x in self.top_heroes[:num_heroes]])  # Filter heroes
        if id == 1:
            pass
        elif id == 2:
            pass
        elif id == 3:
            return func_3(graph, kwargs['seq'], kwargs['endpoints'])
        elif id == 4:
            return func_4(graph, kwargs['hero_1'], kwargs['hero_2'])
        elif id == 5:
            pass
        else:
            raise ValueError('There is no functionality for the chosen id.')
