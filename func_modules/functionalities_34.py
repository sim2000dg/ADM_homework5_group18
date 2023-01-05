import pickle
import networkx as nx
from collections import deque
from networkx.algorithms.flow import edmonds_karp


# The main idea behind this functionality is basically BFS, we explore the graph until we find the node which
# is our target one, repeatedly. Basically, we start from the start node, than we get to the second one in the line with
# BFS (a version which saves the path from the source/start to the target); than the source becomes the second node and
# the target the third, and so on.


def func_3(graph: nx.Graph, seq: list[str, ...], endpoints: list[str, str]):
    seq = [endpoints[0]] + seq + [endpoints[1]]  # The overall order
    walk = list()  # Initialize list holding the walk as sequence of labels

    for idx in range(
            len(seq) - 1):  # Iterate through the index of the steps (sequence of nodes we have to pass through)
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
                elif neighbor != target and neighbor not in seq[idx + 1:]:
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


def func_4(graph: nx.Graph, hero_1: str, hero_2: str):
    try:
        nx.get_edge_attributes(graph, 'weight')
    except KeyError:
        graph = graph.copy()
        nx.set_edge_attributes(graph, values=1, name='weight')

    if not nx.has_path(graph, hero_1, hero_2):
        print('The two nodes have no path connecting them, the graph is already partitioned. No cuts are required.')
        return [0, []]
    # This stems from max flow min cut theorem
    residual_network = edmonds_karp(graph, hero_1, hero_2, 'weight')
    flow_dict = nx.get_edge_attributes(residual_network, 'flow')
    cap_dict = nx.get_edge_attributes(residual_network, 'capacity')
    res_dict = {(x, y): cap_dict[(x, y)] - flow_dict[(x, y)] for x, y in residual_network.edges}

    # BFS to find reachable nodes from the source (given the residual graph)
    bfs_queue = deque([hero_1])
    visited = dict()  # The keys of visited will be the nodes in one of the two partitions (the visited nodes)
    visited[hero_1] = True  # Source marked as visited
    while bfs_queue:
        out = bfs_queue.popleft()
        for neighbor in residual_network.neighbors(out):
            if res_dict[(out, neighbor)] > 0 and not visited.get(neighbor):
                visited[neighbor] = True
                bfs_queue.append(neighbor)
            else:
                pass
    cut_1 = visited.keys()
    cut_2 = [x for x in graph.nodes if x not in cut_1]
    cut_set = list(nx.edge_boundary(graph, cut_1, cut_2))
    return len(cut_set), cut_set, \
        nx.subgraph_view(graph, filter_edge=lambda x, y: (x, y) not in cut_set and (y, x) not in cut_set)


if __name__ == '__main__':
    with open('../graphs.pickle', 'rb') as file:
        hero_graph, hero_comics_graph = pickle.load(file)
    # hero_seq = ['ABOMINATION/EMIL BLO', 'HULK/DR. ROBERT BRUC', 'IRON MAN/TONY STARK', 'SPIDER-MAN/PETER PARKER']
    # print(func_3(hero_comics_graph, hero_seq, ('CAPTAIN AMERICA', 'CAPTAIN MARVEL/CAPTA')))
    a, _, _ = func_4(hero_graph, 'IRON MAN/TONY STARK', 'HARKNESS, AGATHA')
    print(a)
