## GOAL: O(E + V)
import csv
import os, sys
import time
from collections import defaultdict
from copy import deepcopy

class Graph():
    '''
        Graph object
        inputs:
            data: json-like dict representing the nodes and edges
        
        Let's take the following simple graph as an example:
                            (A) - (B) - (C)

            edges: (dict of sets) contains every node and its edges, it's also the expected input
                e.g.    {A: {B}, B:{A,C}, C:{B}}

            degrees: (dict of sets) for every degree d in the graph has a list containing the ids of every node with such degree
                e.g.    {1: {A,C}, 2:{B}}
                        means nodes A and C have degree 1, and node B has degree 2

            nodes: (dict of ints) keeps track of the degree of each node, essentially the dual of degrees
                e.g.    {A: 1, B: 2, C: 1}

            n_edges: (int) total number of edges in the graph
                e.g.    One edge from A to B, one edge from B to C => 2 edges

            n_nodes: (int) total number of nodes in the graph
                e.g.    There are 3 nodes: A, B and C

            density: (float) represents the average degree density of the graph, i.e. (number of edges) / (number of nodes)
                e.g.    2 edges and 3 nodes => density = 2/3
    '''
    edges = {}
    nodes = {}
    degrees = defaultdict(set)

    n_edges = 0
    n_nodes = 0
    density = float(0)
    
    def __init__(self, data = {}):
        ### Complexity of initialiation: O( V + E ) (i.e. size of data)

        for k,v in data.items():
            # interesting little tidbit: the whole thing breaks when we try to add self edges
            # this raises the question: to consider a graph to be dense, shall we only consider the outgoing edges,
            # i.e. ignore the self-referencing ones? how about duplicated edges?
            # e.g. let G1 be a graph with 5050 edges between two nodes 
            # and G2 a graph with 100 inter-connected nodes
            # thus density(G1) = 5050/2, density(G2) = 5050/100
            # is G1 denser than G2 because of the amount of edges between the two nodes?
            # or should G2 be denser since it has more nodes densely packed?

            # here we're going with the different nodes approach - in fact we ignore both self edges and multiply-connected nodes
            # just for the sake of making things easier
            self.edges[k] = set(filter(lambda x: x != k, map(str, v)))


        ### Writing to degrees
        for v, e in data.items():
            d = len(e)
            self.degrees[d].add(v)
            self.nodes[v] = d

        # NOTE: since we're building an undirected graph and duplicating every edge,
        #       we must divide n_edges by 2 to take that into account
        
        self.n_nodes = len( self.nodes ) # O(V)
        self.n_edges = int( sum( map( len, self.edges.values() ) ) / 2 ) # O(E)

        self.__update_avg_degree_density()

    def minimum_degree(self):
        '''
            Returns the smallest entry in self.degrees
        '''
        return min(self.degrees)

    def remove_node(self, v):
        '''
            Removes a node v from the graph, i.e. the node itself and its edges
            by updating the edges, degrees and nodes to reflect on such changes

            NOTE: Complexity is O(e_v), where e_v is the number of edges for the node v
                    by looping over every node we essentially get O(E)
        '''

        # For each node connected to v, we remove it from their edges
        for n in self.edges[v]:
            self.edges[n].remove( v )                   # O(1) with a set

            # Updating their position on the degrees list
            degree_n = self.nodes[n]
            self.degrees[ degree_n ].remove( n )        # O(1) with a set
            
            # Removing the entry for this specific degree in case it's now empty
            if not self.degrees[ degree_n ]:
                del self.degrees[ degree_n ]            # O(1) with a set
            
            # And updating the overall data
            self.nodes[n] -= 1
            self.n_edges  -= 1
            self.degrees[ self.nodes[n] ].add( n )      # O(1) with a set
        
        # Removing the node v from the graph
        self.n_nodes -= 1
        del self.edges[v]                               # O(1) with a dict
        del self.nodes[v]                               # O(1) with a dict

        self.__update_avg_degree_density()


    def __update_avg_degree_density(self):
        '''
            Calculates the average degree density of the graph, and saves it on the density attribute
            where average degree density = (number of edges) / (number of nodes)
            and updates it to the density attribute
        '''
        self.density = self.n_edges / self.n_nodes if self.n_nodes else 0 # sanity check


    def __str__(self):
        res = f"nodes: {' '.join(self.edges.keys())}\n" +\
              f"\nnumber of nodes: {self.n_nodes}\n" +\
              f"number of edges: { self.n_edges } \n" +\
              f"density: {self.density}"
            #   f"edges: {self.edges}\n"

        
        return res    


# algorithm itself:
def densest_subgraph(data):
    '''
        Densest Subgraph Algorithm
        Essentially has two parts:
            First scan the graph to calculate its max density
            Then repeat the algorithm until we've achieved the max density

        Complexity analysis
            build graph:                 O ( V + E )
            find max density:            O ( V + E )
            rebuild graph:               O ( V + E )
            reduce graph to max density: O ( V + E )

        So it has linear complexity
    '''

    print("\tBuilding the graph...")
    start = time.time()
    G = Graph(data)
    end = time.time()
    print("\tGraph building time:", end-start,'\n')


    print("\tFinding max density")
    max_den = 0
    start = time.time()
    # repeat while G isn't empty
    while G.edges:
        # find v in G with minimum degree d_G
        min_deg = G.minimum_degree()
        min_nodes = G.degrees[min_deg]
        v = min_nodes.pop()
        
        if not G.degrees[min_deg]:
            del G.degrees[ min_deg ]
        
        G.remove_node(v) # remove v and its edges from G

        if G.density > max_den:
            max_den = G.density
            # print("Density:",max_den)

    end = time.time()
    print("\tAlgorithm duration:", end-start,'\n')


    print("\tRebuilding graph...")
    start = time.time()
    G = Graph(data)
    end = time.time()
    print("\tGraph building time:", end-start,'\n')


    # repeat while current density is not the max density (and while G is not empty)
    print("\tRe-doing the steps until max density")
    start = time.time()
    while G.density != max_den and G.edges:
        min_deg = G.minimum_degree()
        min_nodes = G.degrees[min_deg]
        v = min_nodes.pop()
        
        if not G.degrees[min_deg]:
            del G.degrees[ min_deg ]

        G.remove_node(v)

    end = time.time()
    print("\tElapsed time:", end-start,'\n')
    return G


if __name__ == "__main__":
    files = {
            'example': ('data/k-cores-example.csv', ','),
            'twitch': ('data/twitch.csv', ','),
            'facebook': ('data/facebook.txt', ' '),
            'wiki': ('data/wikispeedia.tsv', ','),
            'california': ('data/roadNet-CA.txt', '\t'),
            'internet': ('data/internet_topology.csv', '\t'),
    }

    try:
        opt = sys.argv[1]
    except IndexError:
        raise Exception(f"You need to specify the file! Options: {', '.join(files.keys())}")


    try:
        files = [files[opt]]
    except KeyError:
        raise Exception(f"{opt} not found! Did you remember to extract data.rar? Remember the available options are: {', '.join(files.keys())}")


    project_path = os.getcwd()

    for f, sep in files:
        print(f"FILE: {f}")
        path = os.path.join(project_path, f)

        # reading complexity: O( V + E ) (aka number of lines in the file)
        print("Reading file...")
        start = time.time()

        with open(path) as f:
            csvfile = csv.reader(f, delimiter=sep)
            data = defaultdict(list)
            for n, t in csvfile:
                data[n].append(t)
                data[t].append(n)

        end = time.time()
        print("Elapsed time:", end-start,'\n')
        
        print("Running densest subgraph algorithm...")
        start = time.time()
        H = densest_subgraph(data)
        end = time.time()

        orig_V = len(data)
        orig_E = int(sum(map(len, data.values()))/2)
        print("V:", orig_V)
        print("E:", orig_E)
        print("V + E:", orig_V + orig_E)
        print()

        print(H)
        
        print("Total algorithm elapsed time:", end - start,'\n')
