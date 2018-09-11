import json
import os
import ndex2
import ndex2.client as nc

file = 'Noonan syndrome.cx'
server = 'dev.ndexbio.org'
username = 'cc.zhang'
password = 'cc.zhang'
UUID = '9a2522ca-e50d-11e7-a019-06832d634f41'
#'4ae77d81-8399-11e8-8b82-525400c25d22'

def create_graphml_from_cx_file(data_file):
    file = open(data_file)
    json1_str = file.read()
    json1_data = json.loads(json1_str)
    clean_json(json1_data)


def create_graphml_from_server(server, UUID, username=None, password=None):
    my_ndex = nc.Ndex2(server, username=username, password=password)
    response = my_ndex.get_network_as_cx_stream(UUID)
    raw_cx = response.json()
    clean_json(raw_cx)

def clean_json(json1_data):
    new_json = {}
    for data in json1_data:
        for key, value in data.items():
            if key == "nodes":
                new_json[key] = value
            if key == "edges":
                new_json[key] = value
            if key == "nodeAttributes":
                new_json[key] = value
            if key == "edgeAttributes":
                new_json[key] = value
            if key == "networkAttributes":
                new_json[key] = value

    if new_json.get("nodeAttributes") is not None:
        for attr in new_json["nodeAttributes"]:
            #print(attr)
            for node in new_json["nodes"]:
                if node.get("@id") == attr.get("po"):
                    node[attr.get("n")] = attr.get("v")
                    break
        del new_json["nodeAttributes"]

    if new_json.get("edgeAttributes") is not None:
        for attr in new_json["edgeAttributes"]:
            #print(attr)
            for node in new_json["edges"]:
                if node.get("@id") == attr.get("po"):
                    node[attr.get("n")] = attr.get("v")
                    break
        del new_json["edgeAttributes"]
    create_xml(new_json)


def create_xml(new_json):

    keys_nodes = {}
    keys_edges = {}
    keys_net = {}
    graphml = ""
    for node in new_json["nodes"]:
        node_data = ""
        for node_key, node_value in node.items():
            if node_key == "n":
                node_data = node_data + '<data key = "name">' + str(node_value) + "</data>" + '\n'
            elif node_key == "r":
                node_data = node_data + '<data key = "represents">' + str(node_value) + "</data>" + '\n'
            elif node_key != "@id":
                node_data = node_data + '<data key = "' + str(node_key) + '">' + str(node_value) + "</data>" + '\n'

            if keys_nodes.get(node_key) == None :
                if node_key != "@id":
                    temp = {}
                    if node_key == "n":
                        temp["attr.name"] = "name"
                        temp["id"] = "name"
                    elif node_key == "r":
                        temp["attr.name"] = "represents"
                        temp["id"] = "represents"
                    else:
                        temp["attr.name"] = node_key
                        temp["id"] = node_key
                    temp["attr.type"] = type(node_value).__name__
                    temp["for"] = "node"
                    keys_nodes[node_key] = temp

        node_data = '<node id = "' + str(node["@id"]) + '">' + "\n" + str(node_data) + "</node>" + '\n'
        graphml = graphml + node_data

    #print(keys_nodes)


    for edge in new_json["edges"]:
        edge_data = ""
        for edge_key, edge_value in edge.items():
            if edge_key == "i":
                edge_data = edge_data + '<data key = "interaction">' + str(edge_value) + "</data>" + '\n'
            elif edge_key == "@id":
                edge_data = edge_data + '<data key = "key">' + str(edge_value) + "</data>" + '\n'
            elif edge_key != "s" and edge_key != "t":
                edge_data = edge_data + '<data key = "' + str(edge_key) + '">' + str(edge_value) + "</data>" + '\n'

            if keys_edges.get(edge_key) == None:
                if edge_key != "s" and edge_key != "t":
                    temp = {}
                    if edge_key == "@id":
                        temp["attr.name"] = "key"
                        temp["id"] = "key"
                    elif edge_key == "i":
                        temp["attr.name"] = "interaction"
                        temp["id"] = "interaction"
                    else:
                        temp["attr.name"] = edge_key
                        temp["id"] = edge_key
                    temp["attr.type"] = type(edge_value).__name__
                    temp["for"] = "edge"
                    keys_edges[edge_key] = temp


        edge_data = '<edge source = "' + str(edge["s"]) + '" target = "' + str(edge["s"]) + '" >' + "\n" + str(edge_data) + "</edge>" + '\n'
        graphml = graphml + edge_data

    #print(keys_edges)



    net_name = "Untitled"
    if new_json.get("networkAttributes") is not None:
        for netattr in new_json["networkAttributes"]:
            if netattr.get("n") != "name":
                graphml = '<data key = "' + str(netattr["n"]) + '">' + str(netattr["v"]) + "</data>" + '\n' + graphml
            elif netattr.get("n") == "name":
                net_name = netattr.get("v")

            if keys_net.get(netattr["n"]) == None:
                temp = {}
                temp["attr.name"] = netattr["n"]
                temp["attr.type"] = type(netattr["v"]).__name__
                temp["for"] = "graph"
                temp["id"] = netattr["n"]
                keys_net[netattr["n"]] = temp


    graphml = '<graph edgedefault="directed" id="' + net_name + '">' + '\n' + graphml + '</graph>'
    #print(graphml)
    keys_nodes = change_to_proper_data_type(keys_nodes)
    keys_edges = change_to_proper_data_type(keys_edges)
    keys_net = change_to_proper_data_type(keys_net)
    graphml = create_list_xml_keys(keys_net) + graphml
    graphml = create_list_xml_keys(keys_edges) + graphml
    graphml = create_list_xml_keys(keys_nodes) + graphml
    create_final_grapml(graphml)


def change_to_proper_data_type(keys_list):
    for key, value in keys_list.items():
        if value["attr.type"] == "int":
            value["attr.type"] = "integer"
        elif value["attr.type"] == "str":
            value["attr.type"] = "string"
        elif value["attr.type"] == "bool":
            value["attr.type"] = "boolean"
    return keys_list


def create_list_xml_keys(keys_list):

    final_key_xml = ""
    for attr, attr_val in keys_list.items():
        key_xml = "<key"
        for key, value in attr_val.items():
            key_xml = key_xml + ' ' + key + ' = "' + value + '"'
        key_xml = key_xml + "/>"
        final_key_xml = final_key_xml + key_xml
    #print(final_key_xml)
    return final_key_xml

def create_final_grapml(graphml):
    final = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n' + '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">'
    final = final + '\n' + graphml + '\n' + '</graphml>'
    #print(final)

    pid = os.getpid()
    graph_file_name =  str(pid)+"_created_graphml.graphml"
    graph_file = open(graph_file_name, "w+", encoding='utf-8')
    graph_file.write(final)
    graph_file.close()



create_graphml_from_cx_file(file)
create_graphml_from_server(server, UUID)
