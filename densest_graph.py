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
    degrees = defaultdict(set)
    density = float(0)

    n_edges = 0
    n_nodes = 0
    
    def __init__(self, data = {}):
        for k,v in data.items():
            # self.edges[k] = list(map(str, v))

            # interesting little tidbit: the whole thing breaks when we try to add self edges
            # this raises the question: to consider a graph to be dense, shall we only consider the outgoing edges,
            # i.e. ignore the self-referencing ones? how about duplicated edges?
            # e.g. let G1 be a graph with 5050 edges between two nodes 
            # and G2 a graph with 100 inter-connected nodes
            # thus density(G1) = 5050/2, density(G2) = 5050/100
            # is G1 denser than G2 because of the amount of edges between the two nodes?
            # or should G2 be denser since it has more nodes densely packed?
            self.edges[k] = set(filter(lambda x: x != k, map(str, v)))


        ### writing to degrees (O(V))
        for v, e in data.items():
            d = len(e)
            self.degrees[d].add(v)
            self.nodes[v] = d

        # NOTE: since we're building an undirected graph and duplicating every edge,
        #       we must divide n_edges by 2 to take that into account
        
        self.n_nodes = len( self.nodes ) # O(V)
        self.n_edges = sum( map( len, self.edges.values() ) ) / 2 # O(E)

        self.update_avg_degree_density()

    def copy(self):
        '''
            Creates a new graph with same attributes

            WARNING: has linear complexity, can become quite dangerous if ran in a loop
        '''
        H = Graph(self.edges)

        return H


    def minimum_degree(self):
        '''
            Returns a tuple of the minimum degree and the nodes corresponding to such degree,
            i.e. (min_deg, min_nodes), where min_deg is an int, and min_nodes a list of node ids
        '''
        # We have to filter out the empty entries in the degrees list
        # otherwise we could return an empty list

        ### TODO: this is O(V), in the O(V+E) loop makes it quadratic
        ### alt idea: attr for Graph keeping track of what the min degree is
        return min(self.degrees)

    def remove_node(self, v):
        '''
            Removes a node v from the graph, i.e. the node itself and its edges
            by updating the edges, degrees and nodes to reflect on such changes
        '''

        ### TODO: in the long run, O(E + V) since we're looking at every node connected to V to remove it from the graph;

        for n in self.edges[v]:
            ### NOTE: assuming we don't have multiple edges bc that complicates things
            degree_n_v = 1
            self.edges[n].remove( v )                   # O(1) with a set

            # updating their position on the degrees list
            self.degrees[ self.nodes[n] ].remove( n )   # O(1) with a set
            if not self.degrees[ self.nodes[n] ]:       # O(1) with a set
                del self.degrees[ self.nodes[n] ]       # O(1) with a set
            
            self.nodes[n] -= degree_n_v
            self.n_edges  -= degree_n_v
            self.degrees[ self.nodes[n] ].add( n )      # O(1) with a set
        
        # removing their references from the dicts
        self.n_nodes -= 1
        del self.edges[v]                               # O(1) with a dict
        del self.nodes[v]                               # O(1) with a dict


    def update_avg_degree_density(self):
        '''
            Calculates the average degree density of the graph, and saves it on the density attribute
            where average degree density = (number of edges) / (number of nodes)
        '''
        self.density = self.n_edges / self.n_nodes if self.n_nodes else 0 # sanity check


# algorithm itself:
def densest_subgraph(graph):
    '''
        Densest Subgraph Algorithm
        Essentially has two parts:
            First scan the graph to calculate its max density
            Then repeat the algorithm until we've achieved the max density

        Best case complexity:   O(V + E),       linear
        Worst case complexity:  O(2*(V + E)),   which is still linear but... eeeeeh
    '''

    G = graph.copy()
    max_den = 0

    # repeat while G isn't empty
    while G.edges:
        # find v in G with minimum degree d_G
        min_deg = G.minimum_degree()
        min_nodes = G.degrees[min_deg]
        v = min_nodes.pop()
        
        if not G.degrees[min_deg]:
            del G.degrees[ min_deg ]
        
        G.remove_node(v) # remove v and its edges from G
        G.update_avg_degree_density() # updating the density
        
        if G.density > max_den:
            max_den = G.density
            # print("Density:",max_den)

            ### NOTE: this was the old solution, however the deepcopy at nearly every loop destroys the performance
            # H = G.copy()

    G = graph.copy()

    # repeat while current density is not the max density (and while G is not empty)
    while G.density != max_den and G.edges:
        min_deg = G.minimum_degree()
        min_nodes = G.degrees[min_deg]
        v = min_nodes.pop()
        
        if not G.degrees[min_deg]:
            del G.degrees[ min_deg ]


        G.remove_node(v)
        G.update_avg_degree_density()

    return G



### IDEAS:
# lemma:
# O being densest subgraph, then for all v in O, degree(v) >= avg_density(O)
# e.g. if avg_density(G) = 1.5, we know that any node with degree < 1.5 is not in the densest graph, so remove them all
# dunno if it's helpful but it could do something ?

### NOTE: certainly helps with looking for the min degree, but still has to go and remove all the nodes so
# I don't think it helps much; point is to make these steps O(1)


if __name__ == "__main__":
    ### READING INPUT FILE
    option = 0

    if len(sys.argv) == 2:
        option = sys.argv[1]

        if option == 'example':
            opt = 0
        elif option == 'twitch':
            opt = 1
        elif option == 'facebook':
            opt = 2
        elif option == 'wiki':
            opt = 3
        elif option == 'internet':
            opt = 4
        else:
            raise Exception(f"{sys.argv[1]} not an option!\nAvailable options: example, twitch, facebook, wiki, internet (leave empty for all of them)")
        
    

    files = [
            ('k-cores-example.csv', ','),
            ('twitch/ENGB/musae_ENGB_edges_edit.csv', ','),
            ('facebook/facebook_combined.txt', ' '),
            ('wikispeedia_paths-and-graph/links_edit.tsv', ','),
            ('internet_topology/as-skitter-edit.csv', '\t'),
        ]

    if option:
        files = [files[opt]]

    project_path = os.getcwd()

    for f, sep in files:
        print(f"FILE: {f}")
        path = os.path.join(project_path, f)

        start = time.time()
        # reading complexity: O(number of lines)
        with open(path) as f:
            csvfile = csv.reader(f, delimiter=sep)
            data = defaultdict(list)
            for n, t in csvfile:
                data[n].append(t)
                data[t].append(n)
        end = time.time()
        print("Read time:", end-start)

        start = time.time()
        graph = Graph(data)
        end = time.time()
        print("Arranging time:", end-start)

        start = time.time()
        H = densest_subgraph(graph)
        end = time.time()

        print("Densest subgraph algorithm time:", end - start)
        print()



    
