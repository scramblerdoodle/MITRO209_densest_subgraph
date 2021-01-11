## GOAL: O(E + V)
import csv
import os, sys
from collections import defaultdict
from copy import deepcopy

class Graph():
    '''
        Graph object
        inputs:
            data: json-like dict representing the nodes and edges
        
        Let's take the following simple graph as an example:
                            (A) - (B) - (C)

            edges: (dict of lists) contains every node and its edges, it's also the expected input
                e.g.    {A: [B], B:[A,C], C:[B]}

            degrees: (dict of lists) for every degree d in the graph has a list containing the ids of every node with such degree
                e.g.    {1: [A,C], 2:[B]}
                        means nodes A and C have degree 1, and node B has degree 2

            nodes: (dict of ints) keeps track of the degree of each node, essentially the dual of degrees
                e.g.    {A: 1, B: 2, C: 1}

            density: (float) represents the average degree density of the graph, i.e. (number of edges) / (number of nodes)
                e.g.    2 edges and 3 nodes => density = 2/3
    '''
    edges = {}
    nodes = {}
    degrees = defaultdict(list)
    density = float(0)
    
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
        '''
            Runs a deepcopy in each attribute of the graph and returns a new one
            (avoids issues when messing around with memory addresses)

            WARNING: has linear complexity, can become quite dangerous if ran in a loop
        '''
        H = Graph()
        H.edges     = deepcopy(self.edges)
        H.nodes     = deepcopy(self.nodes)
        H.degrees   = deepcopy(self.degrees)
        H.density   = self.density

        return H


    def minimum_degree(self):
        '''
            Returns a tuple of the minimum degree and the nodes corresponding to such degree,
            i.e. (min_deg, min_nodes), where min_deg is an int, and min_nodes a list of node ids
        '''
        # We have to filter out the empty entries in the degrees list
        # otherwise we could return an empty list
        return min(filter(lambda x: x[1], self.degrees.items()))

    def remove_node(self, v):
        '''
            Removes a node v from the graph, i.e. the node itself and its edges
            by updating the edges, degrees and nodes to reflect on such changes
        '''
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
        '''
            Calculates the average degree density of the graph, and saves it on the density attribute
            where average degree density = (number of edges) / (number of nodes)
        '''
        # NOTE: since we're building an undirected graph and duplicating every edge,
        #       we must divide n_edges by 2 to take that into account

        n_edges = sum( map( len, self.edges.values() ) )/2 # O(E)
        n_nodes = len(self.edges) # O(V)        

        self.density = n_edges / n_nodes if n_nodes else 0 # sanity check


# algorithm itself:
def densest_subgraph(G, target = -1):
    '''
        Densest Subgraph Algorithm
    '''
    G = G.copy()
    max_den = 0

    # repeat while G isn't empty and current density is not our target density
    while G.edges and max_den != target:

        # find v in G with minimum degree d_G
        min_deg, min_nodes = G.minimum_degree()
        v = min_nodes.pop()
        
        G.remove_node(v) # remove v and its edges from G
        G.avg_degree_density() # updating the density
        
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



    
