from os.path import isfile, expanduser
import sys
sys.path.append("/Users/dexter/Projects/ndex2-client")
import ndex2
import json
nicecx = ndex2.NiceCXNetwork
Ndex2 = ndex2.Ndex2


def load_tutorial_config(connection_name=None):
    username = None
    password = None
    server = "public.ndexbio.org"
    my_ndex2_client = None
    config_file = expanduser("~/ndex_tutorial_config.json")
    save_tutorial_networks_to_my_account = True

    if(isfile(config_file)):
        file = open(config_file, "r")
        config = json.load(file)
        file.close()
        connections = config.get("connections")
        if connections and connections.length > 1:
            if connection_name:
                connection = connections.get(connection_name)
                if connection and connection.get("password") and config.get("username"):
                    if connection.get("server"):
                        server = connection.get("server")
                    username = connection.get("username")
                    password = connection.get("password")

            else:
                print("Error: " + str(connection_name) + " does not define both username and password")

        else:
            print("Error: " + config_file + " does not define any connections")
    else:
        print("Error: " + config_file + " was not found")

        #
    try:
        # Test the connection
        my_ndex=Ndex2(server, username, password)
        tutorial_private_network_uuid = ""
        private_network_cx = my_ndex.
        my_ndex.update_status()
        networks = my_ndex.status.get("networkCount")
        users = my_ndex.status.get("userCount")
        groups = my_ndex.status.get("groupCount")
        print("my_ndex client: %s networks, %s users, %s groups" % (networks, users, groups))
        # TODO - check that user can access private account details

    except Exception as inst:
        print("Could not access account %s with password %s" % (username, password))
        print(inst.args)

    return (server, username, password)