__author__ = 'dexter'

import ndex.client as nc
import ndex.beta.toolbox as toolbox
import ndex.beta.layouts as layouts
import ndex.networkn as networkn
import requests
import argparse, sys

indra_edge_types = ["Acetylation",
                    "Dephosphorylation",
                    "Phosphorylation",
                    "RasGef",
                    "Ribosylation",
                    "Ubiquitination"
                    ]

def main():
    parser = argparse.ArgumentParser(description='format indra network')

    parser.add_argument('username' )
    parser.add_argument('password')
    parser.add_argument('server')
    parser.add_argument('source')
    parser.add_argument('-t',
                    action='store',
                    dest='template_id',
                    help='network id for the network to use as a graphic template')
    parser.add_argument('-l',
                    action='store',
                    dest='layout',
                    help='name of the layout to apply')
    parser.add_argument('-u',
                    action='store',
                    dest='update',
                    help='update instead of creating new')

    arg = parser.parse_args()


    # set up the ndex connection
    # error thrown if cannot authenticate
    my_ndex = nc.Ndex("http://" + arg.server, arg.username, arg.password)

    response = my_ndex.get_network_as_cx_stream(arg.source)
    cx = response.json()
    network = networkn.NdexGraph(cx)

    if arg.layout:
        layouts.apply_directed_flow_layout(network, directed_edge_types=indra_edge_types)

    template_network = None
    if arg.template_id:
        response = my_ndex.get_network_as_cx_stream(arg.template_id)
        template_cx = response.json()
        template_network = networkn.NdexGraph(template_cx)
        toolbox.apply_network_as_template(network, template_network)

    if arg.update:
        my_ndex.update_cx_network(network.to_cx_stream(), arg.source)
    else:
        my_ndex.save_cx_stream_as_new_network(network.to_cx_stream())

if __name__ == '__main__':
    main()








