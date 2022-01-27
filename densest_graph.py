## GOAL: O(E + V)
import csv
import os, sys
import time
from collections import defaultdict

class Graph():
    '''
        Graph object
        inputs:
            filepath:           path to .csv/.txt/.tsv representing the edges
            sep:                separator between values in said file
            nodes_to_remove:    used when rebuilding the graph, so as to not insert a node which is meant to be removed in the final densest solution

        Let's take the following simple graph as an example to explain the attributes:
                            (A) - (B) - (C)

            edges: (dict of sets) contains every node and its edges
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

            min_deg: (int) keeps track of what's the current minimum degree, avoiding re-calculating this at every iteration of the algorithm
                e.g.    min_deg = 1 becase deg(A) = deg(C) = 1 < deg(B) = 2
    
    A priori the building phase should be O(E + V), as it:
        1) loops once over all edges to build the self.edges attribute, only running O(1) functions therein
        2) then loops once over all nodes to build the rest of the attributes, also only running O(1) functions (yes, len() is O(1)) 
    '''
    def __init__(self, filepath = '', sep = '', nodes_to_remove = set()):
        self.edges = defaultdict(set)
        self.degrees = defaultdict(set)
        self.nodes = defaultdict(int)

        self.n_edges = 0
        self.n_nodes = 0
        self.density = float(0)
        self.min_deg = -1
        
        # We're transforming the graph into a simple graph
        with open(filepath) as f:
            csvfile = csv.reader(f, delimiter=sep)
            for n, t in csvfile:
                if n != t: # Ignore self-loops
                    # To simplify the "rebuilding the graph" part of the code
                    if n not in nodes_to_remove and t not in nodes_to_remove:       # O(1) because it's a set
                        # Add each edge once but make it bi-directional (by adding it both to the origin and the target)
                        self.edges[n].add(t)        # O(1) because it's a set
                        self.edges[t].add(n)        # O(1) because it's a set

        # Defining the other attributes by looping over all nodes
        for node, edges in self.edges.items():
            d = len(edges)  # degree of this particular node

            self.degrees[d].add(node)   # adding this node to the `degrees` dict
            self.nodes[node] = d    # adding its degree to the `nodes` dict     

            self.n_nodes += 1   # +1 node to total
            self.n_edges += d   # +d edges to total

            # Computing min_deg while we build the initial Graph
            if d < self.min_deg or self.min_deg == -1:
                self.min_deg = d

        # NOTE: since we're building an undirected graph and duplicating every edge,
        #       we must divide n_edges by 2 to take that into account
        self.n_edges = int(self.n_edges/2)

        # And, lastly, computing the initial density
        self.__update_avg_degree_density()

    def remove_node(self, v):
        '''
            Removes a node v from the graph, i.e. the node itself and its edges
            by updating the edges, degrees and nodes to reflect on such changes

            Input:
                v (str): node to be removed from the Graph

            NOTE: Complexity is O(e_v), where e_v is the number of edges for the node v
                    by looping over every node we essentially get O(E)
        '''

        # For each target node t connected to v, we remove v from their edges
        for t in self.edges[v]:
            self.edges[t].remove( v )                   # O(1) with a set

            # Updating their position on the degrees list
            degree_t = self.nodes[t]
            self.degrees[ degree_t ].remove( t )        # O(1) with a set

            # If t's new degree is non-zero, place it accordingly in the `degrees` dict            
            if degree_t - 1 > 0:
                self.degrees[ degree_t - 1 ].add( t )      # O(1) with a set

                # And update min_deg in case t now has a smaller degree than the previous min_deg
                if degree_t - 1 < self.min_deg: 
                    self.min_deg = degree_t - 1
            
            # Updating total number of edges and t's degree
            self.n_edges  -= 1
            self.nodes[t] -= 1

            # Removing the entry for this specific degree in case it's now empty
            if not self.degrees[ degree_t ]:
                del self.degrees[ degree_t ]            # O(1) with a dict

            # Removing t from the graph in case it has no more edges, and also -1 to total number of nodes
            if not self.edges[ t ]: 
                del self.edges[ t ]             # O(1) with a dict
                del self.nodes[ t ]             # O(1) with a dict
                self.n_nodes -= 1
        
        # Removing the node v from the graph
        self.n_nodes -= 1
        del self.edges[v]                               # O(1) with a dict
        del self.nodes[v]                               # O(1) with a dict

        # And, finally, saving the new density
        self.__update_avg_degree_density()


    def __update_minimum_degree(self):
        '''
            Updates the smallest degree in self.degrees if degrees[min_deg] is now empty 
            (i.e. if there are no longer any nodes with the previous minimum degree)
            otherwise, doesn't change anything
        '''
        if self.min_deg not in self.degrees:
            self.min_deg = min(self.degrees)


    def __update_avg_degree_density(self):
        '''
            Calculates the average degree density of the graph, and saves it on the density attribute
            where average degree density = (number of edges) / (number of nodes)
            and updates it to the density attribute
        '''
        self.density = self.n_edges / self.n_nodes if self.n_nodes else 0 # sanity check for the case n_nodes = 0, which happens in the final iteration


    def __str__(self):
        '''
            Prints the Graph in an insightful manner
        '''
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
            Analyses the graph to find its maximum density subgraph,
            and returns which nodes we need to remove to achieve it,
            which we then use to rebuild the maximum density subgraph.

            Overview:
                Has one major loop over all nodes in G (while G has edges == while G has non-empty nodes),
                in said loop we:
                    1) Update the min_deg, which in most cases will be O(1)
                    2) Get some node v with minimum degree
                    3) Remove the node v and its edges (O(e_v), where e_v is the number of edges in v)
                    4) Save that node v in a temporary list `to_remove`
                    5) If new density > previous max density:
                        i) Save new max density
                        ii) Add the `to_remove` nodes to the overall set of nodes to remove
                        iii) Reset the `to_remove` list

            Thus, the complexity is somewhere between O(E) and O(E*log(V)), depending on the update_minimum
        '''
        max_den = self.density
        to_remove = list()
        densest_to_remove = list()
        
        # repeat while G isn't empty
        while self.edges:
            # find v in G with minimum degree d_G
            self.__update_minimum_degree()
            min_nodes = self.degrees[ self.min_deg ]
            v = min_nodes.pop()

            if not self.degrees[self.min_deg]:  del self.degrees[ self.min_deg ]
            
            self.remove_node(v) # remove v and its edges from G
            to_remove.append(v)

            if self.density > max_den:
                max_den = self.density
                densest_to_remove.extend(to_remove)
                to_remove = list()

        return densest_to_remove

def main():
    global files

    opts = sys.argv[1:]
    # if not opts: opts = ['example'] # default arg for debugging
    
    try:
        if 'all' in opts:
            files = files
        else:
            files = {opt: files[opt] for opt in opts}
    except KeyError:
        raise Exception(f"One of the requested files was not found! The available options are: all, {', '.join(files.keys())}")


    project_path = os.getcwd()
    result_G, result_build, result_algo, result_rebuild = {}, {}, {}, {}

    repeat = 1
    for name, file in files.items():
        f = file[0]
        sep = file[1]

        nodes, edges, densities = [], [], []
        build_time, algo_time, rebuild_time = [], [], []

        for t in range(repeat):
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
            G = Graph(path, sep, set(to_remove))
            end = time.time()
            # print("Total rebuild time:", end - start,'\n')
            rebuild_time.append(end-start)

            nodes.append(G.n_nodes)
            edges.append(G.n_edges)
            densities.append(G.density)

            if t < repeat - 1 : del G

        print(f"Avg build time for {repeat} loop{'s' if repeat > 1 else ''}:", sum(build_time)/repeat)
        print(f"Avg algorithm time for {repeat} loop{'s' if repeat > 1 else ''}:", sum(algo_time)/repeat)
        print(f"Avg rebuild time for {repeat} loop{'s' if repeat > 1 else ''}:", sum(rebuild_time)/repeat)

        print(G)
        result_G[name] = {'n_nodes': sum(nodes)/repeat, 'n_edges': sum(edges)/repeat, 'density': sum(densities)/repeat}
        result_build[name] = sum(build_time)/repeat
        result_algo[name] = sum(algo_time)/repeat
        result_rebuild[name] = sum(rebuild_time)/repeat

    print("\nRun in interactive mode (python3 -i) to look in-depth at the last resulting graph object G and to save the results using the save_to_file function")

    return G, result_G, result_build, result_algo, result_rebuild


if __name__ == "__main__":
    global files
    files = {
            'example': ('data/k-cores-example.csv', ','),
            'twitch': ('data/twitch.csv', ','),
            'facebook': ('data/facebook.txt', ' '),
            'wiki': ('data/wikispeedia.tsv', ','),
            'git': ('data/musae_git_edges.csv', ','),
            'deezer': ('data/HR_edges.csv', ','),
            'fb-artist': ('data/artist_edges.csv', ','),
            'dblp':('data/com-dblp.ungraph.txt','\t'),
            'twitter':('data/twitter_combined.txt', ' '),
            'youtube': ('data/com-youtube.ungraph.txt','\t'),
            'google': ('data/web-Google.txt', '\t'),
            'twitch-gamers': ('data/large_twitch_edges.csv', ','),
            'california': ('data/roadNet-CA.txt', '\t'),
            'berkstan':('data/web-BerkStan.txt', '\t'),
            'internet': ('data/internet_topology.csv', '\t'),
            'gplus': ('data/gplus_combined.txt', ' '),
    }

    G, result_G, result_build, result_algo, result_rebuild = main()


def save_to_file(path, dict_G, build_times, algo_times, rebuild_times):
    header = \
        "| SOURCE | SAMPLE # NODES | SAMPLE # EDGES | # NODES IN FINAL SOL | # EDGES IN FINAL SOL | MAX DENSITY | GRAPH BUILDING | ALGORITHM TIME | REBUILD TIME |\n" +\
        "|-|-|-|-|-|-|-|-|-|\n"
    with open(path, mode='w') as f:
        f.write(header)
        for name, graph in dict_G.items():
            line = f"| {name} | ... | ... " +\
                f"| {graph['n_nodes']} | {graph['n_edges']} | {graph['density']} " +\
                f"| {build_times[name]} | {algo_times[name]} | {rebuild_times[name]} |\n"
            f.write(line)
