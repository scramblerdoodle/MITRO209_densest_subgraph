# Densest Subgraph

A small project for the MITRO209 course at Télécom Paris. The goal is to find the densest subgraph for an undirected graph in linear time, using data from the [Stanford Network Analysis Project](http://snap.stanford.edu/data/index.html) as a base.  
P.S.: not a densest k-subgraph because, y'know, NP-complete.

## Getting Started
1. Extract the data.zip file, which contains all the .txt/.csv/.tsv files containing the graphs
2. Run `python3 densest_subgraph.py <option>` to run the densest subgraph algorithm, where *< option >* is one of the following (all contained in data.rar):
    - example: example given in class of a 10-node graph
    - [twitch](http://snap.stanford.edu/data/twitch-social-networks.html): graph representing connections between different English-speaking streamers on Twitch
    - [facebook](http://snap.stanford.edu/data/ego-Facebook.html): friends lists on Facebook 
    - [wiki](http://snap.stanford.edu/data/wikispeedia.html): paths in the online game Wikispeedia
    - [deezer](http://snap.stanford.edu/data/gemsec-Deezer.html):
    - [git](http://snap.stanford.edu/data/github-social.html): A large social network of GitHub developers which was collected from the public API in June 2019
    - [fb-artist](http://snap.stanford.edu/data/gemsec-Facebook.html): data from Facebook pages from November 2017, "Artist" category
    - [dblp](http://snap.stanford.edu/data/com-DBLP.html): DBLP collaboration network
    - [twitter](http://snap.stanford.edu/data/ego-Twitter.html): social circles on Twitter
    - [google](http://snap.stanford.edu/data/web-Google.html): Graph representing websites and hyperlinks between them, released in 2002 by Google
    - [twitch-gamers](): A social network of Twitch users which was collected from the public API in Spring 2018
    - [california](http://snap.stanford.edu/data/roadNet-CA.html): road network of California
    - [youtube](http://snap.stanford.edu/data/com-Youtube.html): Youtube social network
    - [berkstan](http://snap.stanford.edu/data/web-BerkStan.html): Hyperlinks between pages in berkely.edu and stanford.edu
    - [internet](http://snap.stanford.edu/data/as-Skitter.html): internet topology graph from traceroutes ran in 2005
    - [gplus](http://snap.stanford.edu/data/ego-Gplus.html):  'circles' from Google+
    - test: a dummy test with one long chain of 10.000.000 nodes with 2 edges each, i.e. (1) - (2) - ... - (10.000.000)


## Some data comparison

|   SOURCE      | SAMPLE # NODES | SAMPLE # EDGES | # NODES IN FINAL SOL | # EDGES IN FINAL SOL | MAX DENSITY | GRAPH BUILDING | ALGORITHM TIME | REBUILD TIME  |
|---------------|----------------|----------------|----------------------|----------------------|-------------|----------------|----------------|---------------|
| example       | 10             | 16             | 5                    | 10                   | 2.0         | 0.0002892      | 4.673e-05      | 7.1048e-05    |
| twitch        | 7,126          | 35,324         | 459                  | 5475                 | 11.9281     | 0.0399971      | 0.0559620      | 0.01311874    |
| facebook      | 4,039          | 88,234         | 202                  | 15624                | 77.3465     | 0.0654056      | 0.0988130      | 0.03100895    |
| wiki          | 4,592          | 119,882        | 433                  | 17657                | 40.7783     | 0.1252295      | 0.1411073      | 0.06728911    |
| git           | 37,700         | 289,003        | 712                  | 21535                | 30.2458     | 0.2806870      | 0.5125055      | 0.12074136    |
| deezer        | 54,573         | 498,202        | 6331                 | 103675               | 16.3758     | 0.5390763      | 0.9481253      | 0.24147439    |
| fb-artist     | 50,515         | 819,306        | 1724                 | 100219               | 58.1317     | 0.8113021      | 1.4619901      | 0.33634424    |
| dblp          | 317,080        | 1,049,866      | 114                  | 6441                 | 56.5        | 1.6950888      | 2.5251307      | 0.44855189    |
| twitter       | 81,306         | 2,420,766      | 734                  | 50216                | 68.4142     | 2.3562977      | 2.5077772      | 1.05206751    |
| youtube       | 1,134,890      | 2,987,624      | 1828                 | 83296                | 45.5667     | 7.1445305      | 9.1963036      | 1.61077880    |
| google        | 875,713        | 5,105,039      | 240                  | 6523                 | 27.1792     | 8.6076657      | 9.8893492      | 2.17825388    |
| twitch-gamers | 168,114        | 6,797,557      | 4223                 | 579944               | 137.330     | 8.0286374      | 16.444923      | 3.41928672    |
| california    | 1,965,206      | 5,533,215      | 15836                | 26945                | 1.70150     | 10.210648      | 8.6274757      | 3.16409969    |
| berkstan      | 685,230        | 7,600,595      | 392                  | 40535                | 103.406     | 8.4164173      | 11.251940      | 2.79132270    |
| internet      | 1,696,415      | 11,095,298     | 428                  | 38149                | 89.1332     | 19.826223      | 31.412472      | 4.46747422    |
| gplus         | 107,614        | 13,673,453     | 4420                 | 2784255              | 629.922     | 46.264098      | 28.913655      | 32.2313706    |