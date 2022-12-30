import pickle
import networkx as nx
from collections import deque

# The main idea behind this functionality is basically BFS, we explore the graph until we find the node which
# is our target one, repeatedly. Basically, we start from the start node, than we get to the second one in the line with
# BFS (a version which saves the path from the source/start to the target); than the source becomes the second node and
# the target the third, and so on.


def func_3(graph: nx.Graph, seq: list[str, ...], endpoints: list[str, str]):
    seq = [endpoints[0]] + seq + [endpoints[1]]  # The overall order
    walk = list()  # Initialize list holding the walk as sequence of labels

    for idx in range(len(seq)-1):  # Iterate through the index of the steps (sequence of nodes we have to pass through)
        # The queue will not just hold node identifiers but also the list of strings representing the walk 'til them
        bfs_queue = deque([[seq[idx], []]])  # Queue is indeed initialized with starting node and empty list
        target = seq[idx+1]  # Target is the next element in sequence w.r.t. current element
        visited = dict()  # We use a dictionary to keep track of visited nodes (fast and relatively lightweight)
        connected_flag = False  # This boolean flag is needed to handle nodes which have no walk connecting them

        while bfs_queue:  # Until the queue is empty
            out = bfs_queue.popleft()  # Pop from left (combined with append, it is FIFO)
            for neighbor in graph.neighbors(out[0]):  # Iterate through neighbors of current node
                if visited.get(neighbor):  # If neighbor was visited, we go to next iteration
                    pass
                # If neighbor is not target, mark the node as visited and add it to the queue along with
                # the extended walk linking the source to it. We also check that the node is not in the ordered sequence
                elif neighbor != target and neighbor not in seq:
                    visited[neighbor] = 1
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

    return walk


if __name__ == '__main__':
    import random
    with open('../graphs.pickle', 'rb') as file:
        _, hero_comics_graph = pickle.load(file)
    hero_seq = ['ABOMINATION/EMIL BLO', 'HULK/DR. ROBERT BRUC', 'IRON MAN/TONY STARK', 'SPIDER-MAN/PETER PARKER']

    print(func_3(hero_comics_graph, hero_seq, ('CAPTAIN AMERICA', 'CAPTAIN MARVEL/CAPTA')))
