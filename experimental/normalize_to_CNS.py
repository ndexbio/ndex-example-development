
import ndex.client as nc
import ndex.beta.toolbox as toolbox
import ndex.beta.layouts as layouts
import ndex.networkn as networkn
import argparse
import modules.cns_normalize as cns

def main():
    parser = argparse.ArgumentParser(description='normalize network to CNS format')

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

    arg = parser.parse_args()

    # set up the ndex connection
    # error thrown if cannot authenticate
    my_ndex = nc.Ndex("http://" + arg.server, arg.username, arg.password)

    response = my_ndex.get_network_as_cx_stream(arg.source)
    cx = response.json()
    from_network = networkn.NdexGraph(cx)

    from_network.set_name(from_network.get_name() + " normalized")

    to_network = cns.normalize(from_network)

    # add nodes from source to new

    # add edges, transforming to CNS

    if arg.layout:
        layouts.apply_directed_flow_layout(to_network, directed_edge_types=cns.directed_predicates)

    if arg.template_id:
        response = my_ndex.get_network_as_cx_stream(arg.template_id)
        template_cx = response.json()
        template_network = networkn.NdexGraph(template_cx)
        toolbox.apply_network_as_template(to_network, template_network)

    my_ndex.save_cx_stream_as_new_network(to_network.to_cx_stream())

if __name__ == '__main__':
    main()

