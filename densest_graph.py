### DENSEST GRAPH ALGO
## GOAL: O(E + V)
import csv
import os, sys
from collections import defaultdict
from copy import deepcopy

class Graph():
    degrees = defaultdict(list)
    edges = {}
    nodes = {}
    
    def __init__(self, data = {}):
        for k,v in data.items():
            # self.edges[k] = list(map(str, v))
            # interesting little tidbit: the whole thing breaks when we try to add self edges
            # this raises the question: to consider a graph to be dense, shall we only consider the outgoing edges,
            # i.e. ignore the self-referencing ones?
            self.edges[k] = list(filter(lambda x: x != k, map(str, v)))


        ### writing to degrees (O(V))
        for v, e in data.items():
            d = len(e)
            self.degrees[d].append(v)
            self.nodes[v] = d

    def copy(self):
        # This might have a really large complexity idk
        H = Graph()
        H.edges     = deepcopy(self.edges)
        H.nodes     = deepcopy(self.nodes)
        H.degrees   = deepcopy(self.degrees)

        return H


    def minimum_degree(self):
        return min(filter(lambda x: x[1], self.degrees.items()))

    def remove_node(self, v):
        # DEBUG: print('v:', v, 'edges:', self.edges[v])

        for n in self.edges[v]:
            # removing v from the edges of each n
            self.edges[n].remove( v )

            # updating their position on the degrees list
            self.degrees[ self.nodes[n] ].remove( n )
            self.nodes[n] -= 1
            self.degrees[ self.nodes[n] ].append( n )
        
        # removing their references from the dicts
        del self.edges[v]
        del self.nodes[v]


    def avg_degree_density(self):
        # number of edges / number of nodes
        ### TODO IDEAS FOR OPTIMISATION:
        # since we're removing edges and nodes one-by-one,
        # we could keep n_nodes and n_edges as attributes for the class itself and save ourselves some complexity
        n_nodes = len(self.edges) # O(V)
        n_edges = sum( map( len, self.edges.values() ) ) # O(E)
        
        return n_edges / n_nodes if n_nodes else 0 # sanity check


# algorithm itself:
def densest_subgraph(G):
    H = G.copy()

    while G.edges: # i.e. while G isn't empty

        # find v in G with minimum degree d_G
        min_deg, min_nodes = G.minimum_degree()
        v = min_nodes.pop()
        # print("min deg:", min_deg, "v:", v)
        
        G.remove_node(v) # remove v and its edges from G
        ### TODO: THIS IS WHAT'S FUCKING UP THE PERFORMANCE
        if G.avg_degree_density() > H.avg_degree_density():
            # print(f"Density: {G.avg_degree_density()}")
            H = G.copy()

    return H




### IDEAS:
# lemma:
# O being densest subgraph, then for all v in O, degree(v) >= avg_density(O)
# e.g. if avg_density(G) = 1.5, we know that any node with degree < 1.5 is not in the densest graph, so remove them all
# dunno if it's helpful but it could do something ?


### NOTE: twitch final density: 23.857142857142858

if __name__ == "__main__":
    ### READING INPUT FILE (json)
    args = sys.argv

    if len(args) != 2:
        raise Exception(f"{__file__} requires exactly 1 argument (input file)")
    
    path = os.getcwd()
    path = os.path.join(path, sys.argv[1])


    print("Reading file...")
    # reading complexity: O(number of lines)
    with open(path) as f:
        csvfile = csv.reader(f)
        data = defaultdict(list)
        for n, t in csvfile:
            data[n].append(t)
            data[t].append(n)
    
    print("Arranging data...")
    graph = Graph(data)
    
    print("Looking for densest subgraph...")
    
    import time
    start = time.time()
    H = densest_subgraph(graph)
    end = time.time()

    print(H.edges)
    print(H.nodes)
    print("Elapsed time:", end - start)


    
