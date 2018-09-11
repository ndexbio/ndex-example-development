import pandas as pd
import ndex2
import json
import ndex2.client as nc
import os
import numpy as np

server = 'public.ndexbio.org'
username = "cc.zhang"
password = "cc.zhang"
UUID = "ef119635-23da-11e8-b939-0ac135e8bacf"




def create_from_server(server, UUID, username=None, password=None):
    my_ndex = nc.Ndex2(server, username, password)
    cx_stream = my_ndex.get_network_as_cx_stream(UUID)
    raw_cx = cx_stream.json()


    counter = 0
    position_n = 0
    position_e = 0
    position_net = 0
    new_node_attr_list = []
    new_edge_attr_list = []
    context = []
    for section in raw_cx:
        for name_section, info in section.items():
            if name_section == "nodes":
                for node in info:
                    if node.get("@id"):
                        new_attr_n = {}
                        id = node["@id"]
                        new_attr_n["po"] = id
                        new_attr_n["n"] = "cx node id"
                        new_attr_n["v"] = id
                        new_node_attr_list.append(new_attr_n)
                    if node.get("r"):
                        new_attr_r = {}
                        represents = node.get("r")
                        new_attr_r["po"] = node["@id"]
                        new_attr_r["n"] = "ID"
                        new_attr_r["v"] = represents
                        new_node_attr_list.append(new_attr_r)


            if name_section == "edges":
                for edge in info:
                    new_attr = {}
                    id = edge["@id"]
                    new_attr["po"] = id
                    new_attr["n"] = "cx edge id"
                    new_attr["v"] = id
                    new_edge_attr_list.append(new_attr)

            if name_section == "@context":
                temp = {}
                temp["n"] = "@context"
                temp["v"] = info[0]
                context.append(temp)
            if name_section == "nodeAttributes":
                position_n = counter
            if name_section == "edgeAttributes":
                position_e = counter
            if name_section == "networkAttributes":
                position_net = counter
        counter = counter + 1

    raw_cx[position_n].get("nodeAttributes").extend(new_node_attr_list)
    raw_cx[position_e].get("edgeAttributes").extend(new_edge_attr_list)
    raw_cx[position_net].get("networkAttributes").extend(context)

    pid = os.getpid()
    file_name = str(pid) + "fixed_cx.cx"
    key_file = open(file_name, "w+", encoding='utf-8')
    final_graph = json.dumps(raw_cx)
    key_file.write(str(final_graph))
    key_file.close()
    niceCX = ndex2.create_nice_cx_from_file(file_name)
    os.remove(file_name)
    return niceCX

def check_for_vert_bars(df):

    poscol = 0
    for name, values in df.iteritems():
        posrow = 0
        for data_points in values:
            if type(data_points) is str:
                if data_points.find('|') != -1:
                    data_points = data_points.replace('|', " ")
                    df.iloc[posrow, poscol] = data_points
            posrow = posrow + 1
        poscol = poscol + 1

    return df

def cx_to_pandas(niceCx):


    df = niceCx.to_pandas_dataframe()
    #df = df.replace(np.nan, 0)
    df = df.replace({'source_cx node id': np.nan, 'target_cx node id' : np.nan}, 0) #{'a': {'b': np.nan}}
    edges_pandas = pd.DataFrame()
    nodes_pandas = pd.DataFrame()
    net_pandas = pd.DataFrame()
    final_nodes_pandas = pd.DataFrame()
    #df.to_csv('myfile4.csv')


    df = check_for_vert_bars(df)


    poscol = 0
    for name, values in df.iteritems():
        posrow = 0
        for data_points in values:
            if type(data_points) is str:
                if data_points.find('"') != -1 and data_points.find(",") != -1:
                    data_points = data_points.replace(',','|')
                    data_points = data_points.replace('"',"")
                    df.iloc[posrow, poscol] = data_points
                elif data_points.find('"') != -1:
                    data_points = data_points.replace('"', "")
                    df.iloc[posrow, poscol] = data_points
            posrow = posrow + 1

        if name == "source" or name == "target":
            #edges_pandas[name] = values
            nodes_pandas[name] = values
        elif name == "source_cx node id":
            edges_pandas["source cx node id"] = values
            nodes_pandas[name] = values
        elif name == "target_cx node id":
            edges_pandas["target cx node id"] = values
            nodes_pandas[name] = values
        elif "source" in name or "target" in name:
            nodes_pandas[name] = values
        else:
            edges_pandas[name] = values
        poscol = poscol + 1


    #nodes_pandas = nodes_pandas.replace(np.nan, 0, regex=True)

    nodes_organized_s = {}
    nodes_organized_t = {}
    counter_s = 0
    counter_t = 0
    for source_n in nodes_pandas["source_cx node id"]:
        if source_n not in nodes_organized_s:
            nodes_organized_s[int(source_n)] = counter_s
        counter_s = counter_s + 1
    for target_n in nodes_pandas["target_cx node id"]:
        if nodes_organized_s.get(int(target_n)) == None:
            nodes_organized_t[int(target_n)] = counter_t
        counter_t = counter_t + 1


    source_cols = {}
    target_cols = {}
    counter_columns = 0
    for name, values in nodes_pandas.iteritems():
        if name == "source":
            source_cols["name"] = counter_columns
        elif name == "target":
            target_cols["name"] = counter_columns
        elif "source_" in name:
            source_cols[name.replace("source_","")] = counter_columns
        elif "target_" in name:
            target_cols[name.replace("target_","")] = counter_columns
        counter_columns = counter_columns + 1
    #print(source_cols)


    nodes_information = {}
    for columns, col_info in source_cols.items():
        column_info = []
        for node, node_info in nodes_organized_s.items():
            column_info.append(nodes_pandas.iloc[node_info,col_info])
        nodes_information[columns] = column_info
    for columns2, col2_info in target_cols.items():
        column_info2 = []
        for node2, node2_info in nodes_organized_t.items():
            column_info2.append(nodes_pandas.iloc[node2_info,col2_info])
        nodes_information[columns2].extend(column_info2)

    for final_name, final_value in nodes_information.items():
        final_nodes_pandas[final_name] = final_value




            #print(nodes_pandas.iloc[0,0])


    netnames = []
    netvalue = []
    for n_a in niceCx.networkAttributes:
        dictna = str(n_a)
        netattr = json.loads(dictna)
        netnames.append(netattr.get("n"))
        temp = str(netattr.get("v"))
        if temp.find("'") != -1:
            temp = temp.replace("'","")
            temp = temp.replace(",", "|")
            temp = temp.replace("{","")
            temp = temp.replace("}", "")
        netvalue.append(temp)
    net_pandas["name"] = netnames
    net_pandas["value"] = netvalue


    #final_nodes_pandas.to_csv('myfile4.csv')
    reorder(final_nodes_pandas, edges_pandas, net_pandas)


def reorder(nodes_pandas, edges_pandas, net_pandas):

    if "interaction" in edges_pandas:
        order_edges = ['cx edge id', 'source cx node id','interaction','target cx node id']
    else:
        order_edges = ['cx edge id', 'source cx node id', 'target cx node id']

    edges_pandas = edges_pandas[order_edges + [c for c in edges_pandas if c not in order_edges]]

    if "cx node id" in nodes_pandas and "ID" in nodes_pandas:
        order_nodes = ["cx node id", "name", "ID"]
    elif "cx node id" in nodes_pandas:
        order_nodes = ["cx node id", "name"]
    elif "ID" in nodes_pandas:
        order_nodes = ["name", "ID"]

    nodes_pandas = nodes_pandas[order_nodes + [c for c in nodes_pandas if c not in order_nodes]]
    pandas_to_excel(nodes_pandas, edges_pandas, net_pandas)

def pandas_to_excel(nodes_pandas, edges_pandas, net_pandas):
    pid = os.getpid()
    writer = pd.ExcelWriter(str(pid)+'pandas_from_cx.xlsx', engine='xlsxwriter')
    nodes_pandas.to_excel(writer, sheet_name='Nodes')
    edges_pandas.to_excel(writer, sheet_name='Edges')
    net_pandas.to_excel(writer, sheet_name='Network Properties')
    writer.save()

niceCX = create_from_server(server, UUID, username=username, password=password)
cx_to_pandas(niceCX)

