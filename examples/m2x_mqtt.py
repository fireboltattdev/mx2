# Run like this:
#   $ APIKEY=<YOUR APIKEY> DEVICE=<YOUR DEVICE ID> python m2x_mqtt.py

import os
import pprint

from m2x.client import M2XClient
from m2x.v2.api import MQTTAPIVersion2


APIKEY = os.environ['APIKEY']
DEVICE_ID = os.environ['DEVICE']

client = M2XClient(key=APIKEY, api=MQTTAPIVersion2)
device = client.device(DEVICE_ID)

pprint.pprint(device.data)
