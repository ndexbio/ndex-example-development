
import ndex.client as nc
import ndex.beta.toolbox as toolbox
import ndex.beta.layouts as layouts
import ndex.networkn as networkn
import argparse
from modules.cns_normalize import normalize, directed_predicates
from modules.cns_assemble import assemble_networks, remove_one_edge_nodes


def get_network_set(ndex_client, uuid):
    return ndex_client.get('/networkset/' + uuid)

def get_network(ndex_client, uuid):
    response = ndex_client.get_network_as_cx_stream(uuid)
    cx = response.json()
    return networkn.NdexGraph(cx)

def main():
    parser = argparse.ArgumentParser(description='normalize and merge a set of networks')

    parser.add_argument('username' )
    parser.add_argument('password')
    parser.add_argument('server')
    parser.add_argument('set')
    parser.add_argument('-n',
                        action= 'store',
                        dest='to_network_name',
                        default='merged CNS network',
                        help='name of the resulting network')
    parser.add_argument('-t',
                    action='store',
                    dest='template_id',
                    help='network id for the network to use as a graphic template')
    parser.add_argument('-l',
                    action='store',
                    dest='layout',
                    help='name of the layout to apply')
    parser.add_argument('-r',
                    action='store',
                    dest='remove_singletons',
                    help='if true, remove nodes with only one edge')

    arg = parser.parse_args()

    # set up the ndex connection
    # error thrown if cannot authenticate
    my_ndex = nc.Ndex("http://" + arg.server, arg.username, arg.password)

    set = get_network_set(my_ndex, arg.set)
    uuids = set.get('networks')
    assembly_networks = []

    for uuid in uuids:
        network = get_network(my_ndex, uuid)
        print(network.get_name())
        assembly_networks.append(normalize(network))

    to_network = assemble_networks(assembly_networks, arg.to_network_name, "name")

    if arg.layout:
        layouts.apply_directed_flow_layout(to_network, directed_edge_types=directed_predicates)

    if arg.template_id:
        response = my_ndex.get_network_as_cx_stream(arg.template_id)
        template_cx = response.json()
        template_network = networkn.NdexGraph(template_cx)
        toolbox.apply_network_as_template(to_network, template_network)

    if arg.remove_singletons:
        remove_one_edge_nodes(to_network)

    my_ndex.save_cx_stream_as_new_network(to_network.to_cx_stream())

if __name__ == '__main__':
    main()

