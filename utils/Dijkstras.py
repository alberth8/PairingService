import math
from heapq import *
import pandas as pd

# Requires pandas

'''
all_shortest_paths() computes all shortest paths between all nodes in a given adjacency matrix
and returns an object of objects where the key represents the source node and the value is an
object. This inner object's keys are represent the destination node, and it's value is
the path, i.e. - the recommended ingredients.

output:
{
 ...
 source_i: {
    ing_k: [ing_k, ... , source_i],
    ...
    ing_n: [ing_n, ... , source_i]
 },
 ...
 source_p: {
    ... similarly ...
 },
 ...
 }


NOTE on naming clarification: `start` indicates where we are starting to trace backwards, but in
finding the paths (Dijkstra's algorithm), `start` is the end / destination node.
'''


def all_shortest_paths(start, adj_mat, ingredients):

    table = {}
    # for each ingredient, treat it as the source node
    for end in ingredients:  # ingredients is what new_cols is in notebook
        temp = {}  # will store all paths from an ingredient to the source
        prevs = dijkstras(adj_mat, start)['prev']  # finds all shortest paths going to source node
        for i in prevs:  # for each end node, use `get_path` to trace backwards to the source
            temp[i] = get_path(i, end, prevs)['path']
        table[end] = temp

    return table

'''
Dijkstra's algorithm implemented with pandas data frame as representation of graph
'''


def dijkstras(adj_mat, start):
    # Initialize single source
    dist = {}
    prev = {}
    Q = []
    for v in list(adj_mat.columns.values):
        if v == start:
            dist[v] = 0
        else:
            dist[v] = math.inf
            prev[v] = None
        heappush(Q, [dist[v], v])

    while Q:
        through_me = heappop(Q)[1]
        for neighbor in list(adj_mat.index[(adj_mat > 0)[through_me]]):
            new_path_dist = dist[through_me] + adj_mat.loc[through_me, neighbor]  # matrix is symmetric
            # Relaxation
            if new_path_dist < dist[neighbor]:
                dist[neighbor] = new_path_dist
                prev[neighbor] = through_me
                # Decrease priority
                for node in Q:
                    if node[1] == neighbor:
                        node[0] = new_path_dist

    return {'dist': dist, 'prev': prev}


'''
get_path() recursively gets an individual path between two selected nodes
'''


def get_path(here, to_here, all_paths):

    def trace(start, end, start_to_end=[]):
        start_to_end.append(start)

        if start == end:
            return start_to_end

        next_node = all_paths[start]
        return trace(next_node, end, start_to_end)

    return {'start': here, 'end': to_here, 'path': trace(here, to_here)}

