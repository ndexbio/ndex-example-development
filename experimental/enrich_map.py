from .modules.enrichment import enrichment_map
import json
from ndex.networkn import NdexGraph

import argparse

parser = argparse.ArgumentParser(description='perform gene enrichment on a network where some nodes have lists of gene symbols as properties')

parser.add_argument('gene_list_file', action='store')
parser.add_argument('map_network_file', action='store')

parser.add_argument('ndex_output', action='store')
parser.add_argument('username', action='store')
parser.add_argument('password', action='store')

arg = parser.parse_args()

print("loading gene list " + str(arg.gene_list_file))
query_genes = enrichment_map.load_gene_list(arg.gene_list_file)

print("loading map " + str(arg.map_network_file))
with open(arg.map_network_file) as file:
    map_cx = json.load(file)

network_map = NdexGraph(map_cx)

enrichment_map.enrich_map(network_map, query_genes)

# temporary hardcoded output
network_map.write_to("./resources/test_enrich.cx")
