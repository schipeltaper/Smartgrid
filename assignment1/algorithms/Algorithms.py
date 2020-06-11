import sys
import os
sys.path.append(os.path.abspath('../classes'))
from House import House
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

# calculate costs for list of batteries
def totalCosts(batteries):
    total_costs = 0
    for battery in batteries:
        total_costs += battery.costs
    return total_costs
    
def dijkstra_algo(graph, indices):
    dist_matrix, predecessors = dijkstra(graph, directed=False, indices=indices, return_predecessors=True)
    return [dist_matrix, predecessors]

