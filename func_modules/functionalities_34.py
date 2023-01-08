import pickle
import networkx as nx
from collections import deque
from networkx.algorithms.flow import edmonds_karp


# The main idea behind this functionality is basically BFS, we explore the graph until we find the node which
# is our target one, repeatedly. Basically, we start from the start node, than we get to the second one in the line with
# BFS (a version which saves the path from the source/start to the target); than the source becomes the second node and
# the target the third, and so on.


def func_3(graph: nx.Graph, seq: list[str, ...], endpoints: tuple[str, str]) -> list[str, ...]:
    """
    This function finds the shortest ordered walk passing through the given nodes and starting and ending at given
    endpoints. It is a relatively simple but effective implementation, using BFS to find at each iteration the shortest
    path between subsequent nodes in the sequence. Specifically, a version of BFS is used which allows to store the path
    from the source to the target.
    :param graph: A NetworkX graph, undirected and unweighted.
    :param seq: The sequence of nodes we have to pass through in the walk.
    :param endpoints: The endpoints in the walk.
    :return: A list of strings, each a point in the walk (including the endpoints).
    """
    seq = [endpoints[0]] + seq + [endpoints[1]]  # The overall order
    walk = list()  # Initialize list holding the walk as sequence of labels

    for idx in range(len(seq) - 1):  # Iterate through the index of the steps (sequence of nodes we pass through)
        # The queue will not just hold node identifiers but also the list of strings representing the walk 'til them
        bfs_queue = deque([[seq[idx], []]])  # Queue is indeed initialized with starting node and empty list
        target = seq[idx + 1]  # Target is the next element in sequence w.r.t. current element
        visited = dict()  # We use a dictionary to keep track of visited nodes (fast and relatively lightweight)
        connected_flag = False  # This boolean flag is needed to handle nodes which have no walk connecting them
        visited[seq[idx]] = True  # The source is of course marked as visited

        while bfs_queue:  # Until the queue is empty
            out = bfs_queue.popleft()  # Pop from left (combined with append, it is FIFO)
            for neighbor in graph.neighbors(out[0]):  # Iterate through neighbors of current node
                if visited.get(neighbor):  # If neighbor was visited, we go to next iteration
                    pass
                # If neighbor is not target, mark the node as visited and add it to the queue along with
                # the extended walk linking the source to it. We also check that the node is not in the
                # following part of the ordered sequence (order of first visit needs to be maintained)
                # These two things are combined in the following conditional statement.
                # The node in seq[idx+1] is the current target one
                elif neighbor not in seq[idx + 1:]:
                    visited[neighbor] = True
                    bfs_queue.append([neighbor, out[1] + [out[0]]])
                # If neighbor is target, stop BFS by breaking inner and outer loop and add the built path to the walk
                elif neighbor == target:
                    walk.extend(out[1] + [out[0]])
                    connected_flag = True  # Signal to the logic that the node could be reached
                    break
            if connected_flag:
                break

        # If the node could not be reached the boolean flag remains False, and we have to alt the whole execution
        if not connected_flag:
            print('There is no such walk')
            return []

    return walk + [endpoints[1]]


# The main idea here is exploiting the max-flow min-cut theorem (https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem)
# which allow us to link max-flow problems to min-cut problems. In other words we have to disconnect the source from
# the sink inducing a cut/a partition, and we need to do that with the minimum cost possible, thus finding the s-t cut
# with the minimum capacity over the set of all the possible ones.

# Doing that is not trivial and requires some relatively advanced tools. First of all we need to build the residual
# graph, i.e. the graph representing the flow in the maximized scenario. In the original graph, the weight of an edge
# is its capacity, i.e. the maximum amount of flow it can carry. With the residual graph, we have a **directed** graph,
# since the flow has a direction: the residual capacity of each edge is the original capacity - the amount of flow,
# which is negative if the flow goes backwards. In other words, for each original undirected edge we have two directed
# edges. Now, suppose that we can reach a node from the source only using edges with non-null residual capacity:
# we will not be able to reach the sink (otherwise we would have an augmenting path) and the nodes we reach are the ones
# which represent one of the two subsets induced by the minimum s-t cut, i.e. the one with minimum cost/capacity
# disconnecting source and sink. The edges we need to get a cut-set are the ones connecting these reachable nodes to
# the non-reachable ones.


def func_4(graph: nx.Graph, hero_1: str, hero_2: str) -> tuple[int, list[tuple[str, str], ...], nx.Graph]:
    """
    This function computes the minimum s-t cut for a weighted (the graph needs to have edges with a 'weight' attribute)
    undirected graph and for an unweighted undirected graph. It uses the Edmonds-Karp algorithm to compute the maximum
    flow and the residual graph. Breadth-first search is used to get the reachable nodes from the source and thus
    get the actual minimum s-t cut.
    :param graph: A NetworkX graph, weighted undirected or unweighted undirected.
    :param hero_1: The identifier indicating the node used as source.
    :param hero_2: The identifier indicating the node used as sink.
    :return: The number of edges removed, the list of edges removed and the subgraph obtained by removing the edges in
            the cut-set.
    """
    # This allows to understand the graph we are dealing with, if weighted undirected or unweighted undirected.
    if not nx.get_edge_attributes(graph, 'weight'):  # If empty dictionary
        graph = graph.copy()  # Copy to avoid side effect
        # If it is unweighted the edges of the graph have the weight attribute added (homogeneous and = 1)
        nx.set_edge_attributes(graph, values=1, name='weight')

    if not nx.has_path(graph, hero_1, hero_2):  # If source and sink are already disconnected nothing to do
        print('The two nodes have no path connecting them, the graph is already partitioned. No cuts are required.')
        return [0, [], graph]

    # Find residual graph with Edmonds-Karp (weight is the capacity, as already explained)
    residual_network = edmonds_karp(graph, hero_1, hero_2, 'weight')
    flow_dict = nx.get_edge_attributes(residual_network, 'flow')  # Get dictionary for flow attribute
    cap_dict = nx.get_edge_attributes(residual_network, 'capacity')  # Get dictionary for capacity attribute
    # Build dictionary for residual capacity
    res_dict = {(x, y): cap_dict[(x, y)] - flow_dict[(x, y)] for x, y in residual_network.edges}

    # BFS to find reachable nodes from the source (given the residual graph)
    bfs_queue = deque([hero_1])
    visited = dict()  # The keys of visited will be the nodes in one of the two partitions (the visited nodes)
    visited[hero_1] = True  # Source marked as visited
    while bfs_queue:  # Start BFS
        out = bfs_queue.popleft()  # Remove from queue
        for neighbor in residual_network.neighbors(out):  # Iterate over neighbors
            # If edge has non-null residual capacity, it can be used. Checking if node already visited in BFS fashion
            if res_dict[(out, neighbor)] > 0 and not visited.get(neighbor, False):
                visited[neighbor] = True  # Mark as visited
                bfs_queue.append(neighbor)  # Add neighbor to queue
            else:
                pass  # Ignore

    # The keys of the visited dict are the visited nodes and thus the ones in the first subset induced by the cut
    cut_1 = visited.keys()  # First subset (the one with the source)
    cut_2 = [x for x in graph.nodes if x not in cut_1]  # Second subset (the one with the sink)
    cut_set = list(nx.edge_boundary(graph, cut_1, cut_2))  # The set of edges which are cut
    return len(cut_set), cut_set, \
        nx.subgraph_view(graph, filter_edge=lambda x, y: (x, y) not in cut_set and (y, x) not in cut_set)


if __name__ == '__main__':
    with open('../graphs.pickle', 'rb') as file:
        hero_graph, hero_comics_graph = pickle.load(file)
    # hero_seq = ['ABOMINATION/EMIL BLO', 'HULK/DR. ROBERT BRUC', 'IRON MAN/TONY STARK', 'SPIDER-MAN/PETER PARKER']
    # print(func_3(hero_comics_graph, hero_seq, ('CAPTAIN AMERICA', 'CAPTAIN MARVEL/CAPTA')))
    a, _, _ = func_4(hero_graph, 'IRON MAN/TONY STARK', 'HARKNESS, AGATHA')
    print(a)
