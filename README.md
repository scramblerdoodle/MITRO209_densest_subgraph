# Densest Subgraph

A small project for the MITRO209 course at Télécom Paris. The goal is to find the densest subgraph for an undirected graph in linear time, using data from the [Stanford Network Analysis Project](http://snap.stanford.edu/data/index.html) as a base.  
P.S.: not a densest k-subgraph because, y'know, NP-complete.

## Getting Started
1. Unrar the data.rar file, which contains all the .txt/.csv/.tsv files containing the graphs
2. Run `python3 densest_subgraph.py <option>` to run the densest subgraph algorithm, where *< option >* is one of the following (all contained in data.rar):
    - example: example given in class of a 10-node graph
    - [twitch](http://snap.stanford.edu/data/twitch-social-networks.html): graph representing connections between different English-speaking streamers on Twitch
    - [facebook](http://snap.stanford.edu/data/ego-Facebook.html): friends lists on Facebook 
    - [wiki](http://snap.stanford.edu/data/wikispeedia.html): paths in the online game Wikispeedia
    - [deezer](http://snap.stanford.edu/data/gemsec-Deezer.html):
    - [california](http://snap.stanford.edu/data/roadNet-CA.html): road network of California
    - [fb-artist](http://snap.stanford.edu/data/gemsec-Facebook.html): data from Facebook pages from November 2017, "Artist" category
    - [dblp](http://snap.stanford.edu/data/com-DBLP.html): DBLP collaboration network
    - [twitter](http://snap.stanford.edu/data/ego-Twitter.html): social circles on Twitter
    - [youtube](http://snap.stanford.edu/data/com-Youtube.html): Youtube social network
    - [internet](http://snap.stanford.edu/data/as-Skitter.html): internet topology graph from traceroutes ran in 2005


## Some data comparison

| SOURCE      | SAMPLE # NODES | SAMPLE # EDGES | TOTAL SAMPLE SIZE (V + E) | FINAL SOL          | MAX DENSITY | READING TIME    | GRAPH BUILDING | ALGORITHM     | TOTAL ELAPSED TIME |
|-------------|----------------|----------------|---------------------------|--------------------|-------------|-----------------|----------------|---------------|--------------------|
| example     |       10       |       16       |             26            |     V: 5, E:10     |      2      | 0.0001857280731 |    3.17E-05    |    5.20E-05   |   0.0002753734589  |
| twitch      |      7,126     |     35,324     |           42,450          |   V: 459, E:5475   | 11.92810458 |  0.02626872063  |  0.04561161995 | 0.08642625809 |    0.2278988361    |
| facebook    |      4,039     |     88,234     |           92,273          |   V: 202, E:15624  | 77.34653465 |  0.06426644325  |  0.05595946312 |  0.1344313622 |    0.3494474888    |
| wikispeedia |      4,592     |     119,882    |          124,474          |   V: 468, E:18660  | 39.87179487 |   0.1188323498  |  0.09461712837 |  0.1909329891 |    0.5184550285    |
| california  |    1,965,206   |    5,533,214   |         7,498,420         | V: 13835, E: 21569 | 1.559016986 |   7.848263025   |   8.60856843   |  9.616968155  |     35.09157181    |
| internet    |    1,696,415   |   11,095,298   |         12,791,713        |   V:430, E:38341   | 89.16511628 |   13.65575337   |   21.5693469   |  81.23937178  |     199.3052955    |