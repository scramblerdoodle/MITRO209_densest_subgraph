## GOAL: O(E + V)
import csv
import os, sys
import time
from collections import defaultdict

class Graph():
    '''
        Graph object
        inputs:
            data: json-like dict representing the nodes and edges
        
        Let's take the following simple graph as an example:
                            (A) - (B) - (C)

            edges: (dict of sets) contains every node and its edges, it's also the expected input
                e.g.    {A: {B}, B:{A,C}, C:{B}}

            degrees: (dict of sets) for every degree d in the graph has a set containing the ids of every node with such degree
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
    def __init__(self, filepath = '', sep = ''):
        self.edges = defaultdict(set)
        self.nodes = defaultdict(int)
        self.degrees = defaultdict(set)

        self.n_edges = 0
        self.n_nodes = 0
        self.density = float(0)
        self.min_deg = 0
        
        # We're transforming the graph into a simple graph
        with open(filepath) as f:
            csvfile = csv.reader(f, delimiter=sep)
            for n, t in csvfile:
                # Ignore self-loops
                if n != t:
                    # Add each edge once (using sets) but make it bi-directional (by adding it both to the origin and the target)
                    self.edges[n].add(t)
                    self.edges[t].add(n)

        for node, edges in self.edges.items():
            d = len(edges)
            self.degrees[d].add(node)
            self.nodes[node] = d

        self.min_deg = min(self.degrees)
        
        # NOTE: since we're building an undirected graph and duplicating every edge,
        #       we must divide n_edges by 2 to take that into account
        
        self.n_nodes = len( self.nodes )
        self.n_edges = int( sum( map( len, self.edges.values() ) ) / 2 )

        self.__update_avg_degree_density()

    def __update_minimum_degree(self):
        '''
            Returns the smallest entry in self.degrees
        '''
        if self.min_deg not in self.degrees:
            self.min_deg = min(self.degrees)

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
            
            if degree_n - 1 > 0:
                self.degrees[ degree_n - 1 ].add( n )      # O(1) with a set
            
            # Removing the entry for this specific degree in case it's now empty
            if not self.degrees[ degree_n ]:
                del self.degrees[ degree_n ]            # O(1) with a dict

            if not self.edges[ n ]:
                del self.edges[ n ]            # O(1) with a dict
            
            # And updating the overall data
            self.nodes[n] -= 1
            self.n_edges  -= 1

            if self.nodes[n] == 0: del self.nodes[n]
            if 0 < degree_n - 1 < self.min_deg: self.min_deg = self.nodes[n]
        
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
        res = \
            f"\nnumber of nodes: {self.n_nodes}\n" +\
            f"number of edges: { self.n_edges } \n" +\
            f"density: {self.density}\n"
            # f"nodes: {' '.join(self.edges.keys())}\n" +\
            #   f"edges: {self.edges}\n"

        
        return res    

    def densest_subgraph(self):
        '''
            Find maximum density
            Analyses the graph to calculate its max density
            
            Essentially has the same goal as the densest subgraph algorithm,
            but helps in the complexity by breaking it into two different parts
                

            Complexity analysis
                find max density:            O ( V + E )

            So it has linear complexity
        '''
        max_den = 0
        to_remove = []
        densest_to_remove = []
        
        # repeat while G isn't empty
        while self.edges:
            # find v in G with minimum degree d_G
            self.__update_minimum_degree()
            min_nodes = self.degrees[ self.min_deg ]
            v = min_nodes.pop()

            if not self.degrees[self.min_deg]:   
                del self.degrees[ self.min_deg ]
                self.__update_minimum_degree()
            
            self.remove_node(v) # remove v and its edges from G
            to_remove.append(v)

            if self.density > max_den:
                max_den = self.density
                densest_to_remove += to_remove
                to_remove = []

        return densest_to_remove

def main():
    global files

    try:
        opt = sys.argv[1]
    except IndexError:
        raise Exception(f"You need to specify the file! Options: {', '.join(files.keys())}")

    try:
        files = [files[opt]]
    except KeyError:
        raise Exception(f"{opt} not found! Did you remember to extract data.rar? Remember the available options are: {', '.join(files.keys())}")


    project_path = os.getcwd()

    repeat = 1
    nodes = []
    edges = []
    build_time = []
    algo_time = []
    rebuild_time = []
    for t in range(repeat):
        for f, sep in files:
            print(f"FILE: {f}")
            path = os.path.join(project_path, f)

            # print("Building the graph...")
            start = time.time()
            G = Graph(path, sep)
            end = time.time()
            # print("Elapsed time:", end-start,'\n')
            build_time.append(end-start)
            print("Dataset size:","\n\tV:", G.n_nodes,"\n\tE:", G.n_edges, )
            print("\tV + E:", G.n_nodes + G.n_edges)
            # print()

            # print("Looking for the maximum density subgraph...")
            start = time.time()
            to_remove = G.densest_subgraph()
            end = time.time()
            # print("Algorithm elapsed time:", end - start,'\n')
            algo_time.append(end-start)


            # print("Rebuild graph and removing the nodes that were removed during the algorithm...")
            start = time.time()
            G = Graph(path, sep)
            for n in to_remove:
                G.remove_node(n)
            end = time.time()
            # print("Total rebuild time:", end - start,'\n')
            rebuild_time.append(end-start)

            nodes.append(G.n_nodes)
            edges.append(G.n_edges)

            if t < repeat - 1 : del G

    print(f"Avg build time for {repeat} times:", sum(build_time)/repeat)
    print(f"Avg algorithm time for {repeat} times:", sum(algo_time)/repeat)
    print(f"Avg rebuild time for {repeat} times:", sum(rebuild_time)/repeat)

    print(G)

    print("\nRun in interactive mode (python3 -i) to look in-depth at the resulting graph object H")


if __name__ == "__main__":
    global files
    files = {
            'example': ('data/k-cores-example.csv', ','),
            'twitch': ('data/twitch.csv', ','),
            'facebook': ('data/facebook.txt', ' '),
            'wiki': ('data/wikispeedia.tsv', ','),
            'deezer': ('data/HR_edges.csv', ','),
            'fb-artist': ('data/artist_edges.csv', ','),
            'dblp':('data/com-dblp.ungraph.txt','\t'),
            'twitter':('data/twitter_combined.txt', ' '),
            'youtube': ('data/com-youtube.ungraph.txt','\t'),
            'california': ('data/roadNet-CA.txt', '\t'),
            'internet': ('data/internet_topology.csv', '\t'),
    }

    main()