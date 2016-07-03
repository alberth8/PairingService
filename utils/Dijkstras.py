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


def all_shortest_paths(adj_mat, ingredients):

    table = {}
    for source in ingredients: # perform dijkstras on every single node
        print('current source is:', source)
        temp = {}  # will store all paths from an ingredient to the source
        paths_to_source = dijkstras(adj_mat, source)['prev']  # finds all shortest paths going to source node
        for i in paths_to_source:  # for each end node, record path going back to the source. So that should be all nodes except the source node
            temp[i] = get_path(i, source, paths_to_source)['path']
        table[source] = temp

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
            prev[v] = None  # Note: some nodes will not have any neighbors, and so many be left as None; hence KeyError
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

        if not all_paths[start]:
            next_node = end
        else:
            next_node = all_paths[start]  # move to the next node

        # if not next_node: # if doesn't have a next node, don't include it
        #    continue

        return trace(next_node, end, start_to_end)

    return {'start': here, 'end': to_here, 'path': trace(here, to_here)}

