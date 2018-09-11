import lxml.etree as etree
import os
import json

xml_filename = "inputxml.xml"
xsl_filename_graph = "translatorGraph.xsl"
xsl_filename_key = "translatorKeys.xsl"


def xml_to_cx(xml_filename, xsl_filename_graph, xsl_filename_key):
    xslt_docG = etree.parse(xsl_filename_graph)
    trans_graph = etree.XSLT(xslt_docG)

    xslt_docK = etree.parse(xsl_filename_key)
    trans_keys = etree.XSLT(xslt_docK)

    source_doc = etree.parse(xml_filename)

    pid = os.getpid()
    graph_info = trans_graph(source_doc)
    keys_info = trans_keys(source_doc)

    graph_file_name = str(pid)+ "_graph.json"
    graph_file = open(graph_file_name, "w+", encoding='utf-8')
    graph_string = str(graph_info).split("\n",1)[1]
    graph_file.write(graph_string)
    graph_file.close()

    key_file_name = str(pid)+ "_key.json"
    key_file = open(key_file_name, "w+", encoding='utf-8')
    key_string = str(keys_info).split("\n",1)[1]
    key_file.write(key_string)
    key_file.close()

    translate_using_json(graph_string,key_string)
    remove_files(pid)


def remove_files(pid):
    graph_file_name = str(pid) + "_graph.json"
    key_file_name = str(pid) + "_key.json"
    os.remove(graph_file_name)
    os.remove(key_file_name)


def translate_using_json(graph_string, key_string):
    graph_json = json.loads(graph_string)
    key_json = json.loads(key_string)
    final_graph = adjust_nodes(graph_json,key_json)
    final_graph = adjust_edges(final_graph,key_json)
    dict_info = adjust_network(final_graph,key_json)
    final_graph = add_to_beginning(dict_info.get("graph"))
    final_graph = add_to_end(final_graph)

    if  dict_info.get("name") != None:
        file_name = dict_info.get("name") + ".cx"
    else:
        file_name = "Untitled.cx"
    key_file = open(file_name, "w+", encoding='utf-8')
    key_file.write(str(final_graph))
    key_file.close()


def add_to_beginning(final_graph):

    metadata = {"metaData":[]}
    for info in final_graph:
        for key, values in info.items():
            metaDict = {}
            counter = 0
            for data in values:
                counter= counter + 1
            metaDict["name"] = key
            metaDict["elementCount"] = counter
            metaDict["version"] = "1.0"
            metaDict["consistencyGroup"] = 1
            metaDict["properties"] = []
        metadata["metaData"].append(metaDict)
    final_graph.insert(0, metadata)
    num_ver = {"numberVerification": [{"longNumber": 281474976710655}]}
    final_graph.insert(0, num_ver)
    return final_graph

def add_to_end(final_graph):
    status =  {"status": [{"error": "","success": True}]}
    final_graph.append(status)
    return final_graph

def adjust_nodes(graph_json,key_json):
    adjusted_graph = graph_json
    node_list = []
    for node in graph_json[0]["nodes"]:
        node_data = {}
        for key, value in node.items():
            if key == "@id":
                node_data["@id"] = value
            else:
                if key_json[key] == "r" or key_json[key] == "represents":
                    node_data["r"] = value
                elif key_json[key] == "name":
                    node_data["n"] = value
                else:
                    attr_data = {}
                    attr_data["po"] = node_data["@id"]
                    attr_data["n"] = key_json[key]
                    attr_data["v"] = value
                    adjusted_graph[3]["nodeAttributes"].append(attr_data)
        node_list.append(node_data)
    adjusted_graph[0]["nodes"] = node_list
    return adjusted_graph


def adjust_edges(graph_json,key_json):
    adjusted_graph = graph_json
    edge_list = []
    counter = 1
    key_exists = False
    key_exists_name = None

    for single_edge_data_key, single_edge_data_value in graph_json[1]["edges"][0].items():
        if single_edge_data_key != "s" and single_edge_data_key != "t":
            if key_json[single_edge_data_key] == "key":
                key_exists = True
                key_exists_name = single_edge_data_key

    for edge in graph_json[1]["edges"]:
        edge_data = {}
        if key_exists == True:
            edge_data["@id"] = int(edge[key_exists_name])
        for key, value in edge.items():
            if key_exists == False:
                edge_data["@id"] = counter
            if key == "t" or key == "s":
                edge_data[key] = value
            else:
                if key_json[key] == "interaction":
                    edge_data["i"] = value
                else:
                    attr_data = {}
                    if key_json[key] != "key":
                        if key_exists == True:
                            attr_data["po"] = int(edge_data["@id"])
                        else:
                            attr_data["po"] = counter
                        attr_data["n"] = key_json[key]
                        attr_data["v"] = value
                        adjusted_graph[4]["edgeAttributes"].append(attr_data)
        edge_list.append(edge_data)
        counter = counter + 1
    adjusted_graph[1]["edges"] = edge_list
    return adjusted_graph


def adjust_network(graph_json,key_json):
    adjusted_graph = graph_json
    net_list = []
    has_context = False
    name = None

    if key_json.get("title"):
        name = key_json["title"]
        title_graph = {}
        title_graph["n"] = "name"
        title_graph["v"] = name
        net_list.append(title_graph)

    for prop in graph_json[2]["networkAttributes"]:
        for key, value in prop.items():
            if key_json[key] == "__context":
                has_context = True
                context = {"@context": [{value}]}
            if key_json[key] == "name":
                name = value
            attr_data = {}
            attr_data["n"] = key_json[key]
            attr_data["v"] = value
            net_list.append(attr_data)
    adjusted_graph[2]["networkAttributes"] = net_list
    if has_context:
        adjusted_graph.insert(0,context)
    return {"name":name, "graph":adjusted_graph}


xml_to_cx(xml_filename, xsl_filename_graph, xsl_filename_key)

