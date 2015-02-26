# Run like this:
#   $ APIKEY=<YOUR APIKEY> DEVICE=<YOUR DEVICE ID> python m2x_http.py

import os
import pprint

from m2x.client import M2XClient


APIKEY = os.environ['APIKEY']
DEVICE_ID = os.environ['DEVICE']

client = M2XClient(key=APIKEY)
device = client.device(DEVICE_ID)

pprint.pprint(device.data)
