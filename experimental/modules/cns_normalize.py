
import ndex.networkn as networkn
import re
import cns_model as cm


# def make_transform():
#     transform = {}
#     for old, new in predicate_translation.iteritems():
#         transform[unicode(old)] = unicode(new)
#     return transform

# def transform_predicate(predicate, transform):
#     if not predicate:
#         return "interactsWith"
#     for old, new in transform.iteritems():
#         if predicate == old:
#             return new
#     return predicate

wildtypesuffix = re.compile('_wt$', re.IGNORECASE)

def normalize_name(name):
    return wildtypesuffix.sub("", name)


def normalize(from_network):
    ont = cm.predicateOntology(cm.predicates)
    to_network = networkn.NdexGraph()
    to_network.set_name(from_network.get_name())
    node_id_map = {}
    for from_node_id, from_node_attr in from_network.nodes_iter(data=True):
        from_node_attr['name'] = normalize_name(from_node_attr['name'])
        to_node_id = to_network.add_new_node(from_node_attr['name'], from_node_attr)
        node_id_map[from_node_id] = to_node_id


    for from_source_id, from_target_id, source_edge_attr in from_network.edges_iter(data=True):
        to_source_id = node_id_map[from_source_id]
        to_target_id = node_id_map[from_target_id]
        from_predicate = source_edge_attr.get("interaction")
        to_predicate = from_predicate
        to_predicate_object = ont.translate_name(from_predicate)
        to_edge_attr = source_edge_attr.copy()
        if to_predicate_object:
            to_predicate = to_predicate_object.get_name()
            to_edge_attr['directed'] = to_predicate_object.directed
            to_edge_attr['contact'] = to_predicate_object.contact
            to_edge_attr['negative'] = to_predicate_object.negative

        to_network.add_edge_between(to_source_id,
                                    to_target_id,
                                    to_predicate,
                                    to_edge_attr)
    return to_network
