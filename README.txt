working examples:
k-cores-example.csv
twitch/ENGB/musae_ENGB_edges_edit.csv
wikispeedia_paths-and-graph/links_edit.tsv

takes forever but it's there:
internet_topology/as-skitter-edit.csv



Densities and elapsed times: 
source                max density         elapsed time (seconds)            sample size                 total size (V+E)
course example              2                0.0002207756042480         V: 10,      E: 16                     26
twitch              11.928571428571429       1.8021302223205566         V: 7126,    E: 70648                 77.774
facebook            77.34653465346534        2.416614532470703          V: 4039,    E: 88234                 92.273
wikispeedia         48.71910112359551        6.0385119915008545         V: 4592,    E: 239544               244.136
internet-topology   ?????????????????            infinite               V: 1696415, E: 11095298            12.791.713


expected elapsed time:
twitch:         0.660407763260921
facebook:       2.138091933090554
wikispeedia:    5.656965874925443
internet-top:   316.3929627024993       NOT TRUE AT ALL... fuck
