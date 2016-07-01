import math
from heapq import *
import pandas as pd

# Requires pandas


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
