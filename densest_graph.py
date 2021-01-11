## GOAL: O(E + V)
import csv
import os, sys
from collections import defaultdict
from copy import deepcopy

class Graph():
    degrees = defaultdict(list)
    edges = {}
    nodes = {}
    density = 0
    
    def __init__(self, data = {}):
        for k,v in data.items():
            # self.edges[k] = list(map(str, v))
            # interesting little tidbit: the whole thing breaks when we try to add self edges
            # this raises the question: to consider a graph to be dense, shall we only consider the outgoing edges,
            # i.e. ignore the self-referencing ones? how about duplicated edges?
            self.edges[k] = list(filter(lambda x: x != k, map(str, v)))


        ### writing to degrees (O(V))
        for v, e in data.items():
            d = len(e)
            self.degrees[d].append(v)
            self.nodes[v] = d

        self.density = self.avg_degree_density()

    def copy(self):
        # This technically has linear complexity O(V + E) but in the huge while loop for densest_subgraph it becomes quadratic
        H = Graph()
        H.edges     = deepcopy(self.edges)
        H.nodes     = deepcopy(self.nodes)
        H.degrees   = deepcopy(self.degrees)
        H.density   = self.density

        return H


    def minimum_degree(self):
        return min(filter(lambda x: x[1], self.degrees.items()))

    def remove_node(self, v):
        # print('v:', v, 'edges:', self.edges[v])

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
        n_edges = sum( map( len, self.edges.values() ) )/2 # O(E)
        # gotta divide n_edges by 2 to account for the two-sided edges we create when reading the graph
        
        return n_edges / n_nodes if n_nodes else 0 # sanity check


# algorithm itself:
def densest_subgraph(G, target = -1):
    G = G.copy()
    max_den = 0

    # repeat while G isn't empty and current density is not our target density
    while G.edges and max_den != target:

        # find v in G with minimum degree d_G
        min_deg, min_nodes = G.minimum_degree()
        v = min_nodes.pop()
        
        G.remove_node(v) # remove v and its edges from G
        G.density = G.avg_degree_density() # updating the density
        
        if G.density > max_den:
            max_den = G.density

            ### TODO: old solution, however the deepcopy at nearly every loop destroys the performance
            # H = G.copy()

    if max_den == target:
        return G

    return max_den




### IDEAS:
# lemma:
# O being densest subgraph, then for all v in O, degree(v) >= avg_density(O)
# e.g. if avg_density(G) = 1.5, we know that any node with degree < 1.5 is not in the densest graph, so remove them all
# dunno if it's helpful but it could do something ?


### NOTE: twitch final density: 11.928571428571429

if __name__ == "__main__":
    ### READING INPUT FILE
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

    import time
    print("Looking for densest subgraph...")    
    start = time.time()

    # looking for the max density by running the algorithm
    max_den = densest_subgraph(graph)
    # then running it again until we've found this desired density
    H = densest_subgraph(graph, target=max_den)

    end = time.time()

    print("Elapsed time:", end - start)



    
