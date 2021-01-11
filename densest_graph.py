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
def densest_subgraph(G, copy=False):
    H = G.copy()

    while G.edges: # i.e. while G isn't empty

        # find v in G with minimum degree d_G
        min_deg, min_nodes = G.minimum_degree()
        v = min_nodes.pop()
        # print("min deg:", min_deg, "v:", v)
        
        G.remove_node(v) # remove v and its edges from G
        G.density = G.avg_degree_density()
        print(f"Density: {G.density}")
        if G.density > H.density:
            ### TODO: the deepcopy is what's destroying the performance
            # it's actually linear, O(V + E), both spatial and algorithmically, BUT it's in a O(V + E) loop so... yeah
            if copy: 
                H = G.copy()
            else:
                # this is sort of a workaround but it's got a few issues - on the twitch db it misses out 3 nodes for some reason
                # I have a feeling it's because it's not really keeping track of literally every step taken by the algo (removing nodes from G)
                # so there may be a few nodes (namely when the density decreases) which aren't really removed from H and it gets confused
                H.remove_node(v)
                H.density = H.avg_degree_density()

    return H




### IDEAS:
# lemma:
# O being densest subgraph, then for all v in O, degree(v) >= avg_density(O)
# e.g. if avg_density(G) = 1.5, we know that any node with degree < 1.5 is not in the densest graph, so remove them all
# dunno if it's helpful but it could do something ?


### NOTE: twitch final density: 23.857142857142858

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


    import time
    print("Looking for densest subgraph (w/o copy)...")    
    start = time.time()
    H = densest_subgraph(Graph(data), copy=False)
    end = time.time()

    print("\nLooking for densest subgraph (w/ copy)...")
    start2 = time.time()
    H2 = densest_subgraph(Graph(data), copy=True)
    end2 = time.time()

    # print(H.edges)
    # print(H.nodes)
    print("Elapsed time w/ copy:", end - start)
    print("Elapsed time w/o copy:", end2 - start2)


    
