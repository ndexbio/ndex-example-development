import ndex.networkn as networkn
import copy

def merge(from_network, to_network, attribute, node_attribute_id_map, count):
    node_id_map = {}
    #edge_triple_map = {}
    for from_node_id, from_node_attr in from_network.nodes_iter(data=True):
        value = from_node_attr.get(attribute)
        if value:
            ids = to_network.get_node_ids(value, attribute)
            if ids:
                # we found a node with this attribute-value already in the to_network
                # there should only be one, so take the first id in the list
                to_node_id = ids[0]
            else:
                # there is no node in the network with this attribute-value
                # so we need to create one
                to_node_id = to_network.add_new_node(from_node_attr['name'], from_node_attr)

            # having determined the to_node_id corresponding to the from_node_id
            # in from_network, we need to record it for the next phase
            # where we add the edges
            node_id_map[from_node_id] = to_node_id

    for from_source_id, from_target_id, from_edge_attr in from_network.edges_iter(data=True):
        to_source_id = node_id_map[from_source_id]
        to_target_id = node_id_map[from_target_id]
        from_predicate = from_edge_attr.get("interaction")
        to_edge_attr = copy.copy(from_edge_attr)
        to_edge_attr['count'] = count
        to_network.add_edge_between(to_source_id,
                                    to_target_id,
                                    from_predicate,
                                    from_edge_attr)

def assemble_networks(networks, to_network_name, attribute):
    model = networkn.NdexGraph()
    model.set_name(to_network_name)
    node_attribute_id_map = {}
    count = 0
    for network in networks:
        merge(network, model, attribute, node_attribute_id_map, count)
        count+= 1
    return model

def remove_one_edge_nodes(network):
    #   remove nodes with one edge
    for node_id in network.nodes():
        #node_name = network.get_node_attribute_value_by_id(node_id)
        #degree = network.degree([node_id])[node_id]
        number_of_neighbors = len(network.neighbors(node_id))
        #print node_name + " : " + str()
        if number_of_neighbors < 2:
            #print " -- removing " + str(node_name) + " " + str(node_id)
            network.remove_node(node_id)

