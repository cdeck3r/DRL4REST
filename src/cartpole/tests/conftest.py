#
# By convention this file shares common function, fixtures, hooks and others
#

# we need to add the path where OpenAPI's generated server stub is located 
# e.g. DRL4REST/openapi/cartpole/python-flask

import sys, os

here_path = os.path.dirname(os.path.abspath(__file__))

cartpole_pkg = os.path.abspath(here_path + '/../../')
# it must exist
assert os.path.exists(cartpole_pkg)
sys.path.append(cartpole_pkg) 

cartpole_server_stub = os.path.abspath(here_path + '/../../../openapi/cartpole/python-flask')
# it must exist
assert os.path.exists(cartpole_server_stub)
# Finally, we add the generated server stub to PYTHONPATH
sys.path.append( cartpole_server_stub ) 
