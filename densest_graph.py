### DENSEST GRAPH ALGO
## GOAL: O(E + V)
import json
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
        H = Graph()
        H.edges     = deepcopy(self.edges)
        H.nodes     = deepcopy(self.nodes)
        H.degrees   = deepcopy(self.degrees)

        return H


    # aux functions
    def minimum_degree(self):
        # go through all of the nodes and find the smallest one ? - linear, O(E)
        # sort them each time we remove shit from G ? - depends on the algo but prob worse than linear

        # TIP: for each degree d in G, keep a list of nodes with degree d
        # e.g. [0, [8,9,10], [7], [], [1,3,6], [2,4,5]]
        #       0      1      2    3     4        5
        # and after each removal of a node, gotta go -1 on each node connected to it
        # ah fuck this isn't quite as straightforward as I had originally thought
        # something else we could do is save the node's degree as an attr, making it O(1) to find it in the list

        return min(filter(lambda x: x[1], self.degrees.items()))

    def remove_node(self, v):
        nodes = list(map(str, self.edges[v]))
        print('v:', v, 'nodes:', nodes)

        for n in nodes:
            # print("Trying to remove",v,"from",n)
            print(f"Edges of {n}: {self.edges[n]}")
            # removing v from the edges of each n
            # try:
            self.edges[n].remove( v )
            # except ValueError:
            #     pass
                # print(f"Apparently {n} not connected to {v}")
                # print(f"{n} neighbours: {sorted(self.edges[n])}")
            # except KeyError:
            #     pass
                # print(f"{n} is already not in the graph")
        
            # updating their position on the degrees list
            # try:
            self.degrees[ self.nodes[n] ].remove( n )
            self.nodes[n] -= 1
            self.degrees[ self.nodes[n] ].append( n )
            # except ValueError:
                # pass
                # print(f"{n} not in degrees[{self.nodes[n]}]")
            # except KeyError:
                # pass
                # print(f"{n} is already not in nodes")

        # possibly already removed from the degrees list due to the .pop() shit
        # self.degrees[ self.nodes[v] ].remove( v )
        
        del self.edges[v]
        del self.nodes[v]




    def avg_degree_density(self):
        # number of edges / number of nodes

        n_nodes = len(self.edges)
        n_edges = sum( map( len, self.edges.values() ) )
        
        return n_edges / n_nodes if n_nodes else 0


# algorithm itself:
def densest_subgraph(G):
    H = G.copy()

    while G.edges: # i.e. while G isn't empty

        # find v in G with minimum degree d_G
        min_deg, min_nodes = G.minimum_degree()
        v = min_nodes.pop()
        print("min deg:", min_deg, "v:", v)
        
        G.remove_node(v) # remove v and its edges from G
        if G.avg_degree_density() > H.avg_degree_density():
            H = G.copy()

    return H




### IDEAS:
# lemma:
# O being densest subgraph, then for all v in O, degree(v) >= avg_density(O)
# e.g. if avg_density(G) = 1.5, we know that any node with degree < 1.5 is not in the densest graph, so remove them all
# dunno if it's helpful but it could do something ?


if __name__ == "__main__":
    ### READING INPUT FILE (json)
    args = sys.argv

    if len(args) != 2:
        raise Exception(f"{__file__} requires exactly 1 argument (input file)")
    
    path = os.getcwd()
    path = os.path.join(path, sys.argv[1])


    with open(path) as f:
        data = json.loads(f.read())
    
    graph = Graph(data)
    
    H = densest_subgraph(graph)
    print(H.edges)
    print(H.nodes)


    
