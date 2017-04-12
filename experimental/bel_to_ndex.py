import argparse
from os.path import join
import ndex.client as nc
import pybel

parser = argparse.ArgumentParser(description='load a BEL file pybel, convert to CX, then upload to NDEx')

parser.add_argument('username', action='store')
parser.add_argument('password', action='store')
parser.add_argument('server', action='store')
parser.add_argument('directory', action='store')
parser.add_argument('filename', action='store')

args = parser.parse_args()

ndex = nc.Ndex(args.server, args.username, args.password)

path = join(args.directory, args.filename)

print("loading bel")
pybel_graph = pybel.from_path(path, citation_clearing=False)

print("translating to CX")
cx = pybel.to_cx_json(pybel_graph)

print("CX ready")

ndex.save_new_network(cx)
print("Upload to %s account complete" % args.username)
