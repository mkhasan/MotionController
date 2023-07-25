
import math
import sys

import can
import time
from tinymovr.tee import init_tee
from tinymovr.config import get_bus_config, create_device

import time
import datetime;
from datetime import datetime
import pickle
from params import pkl_filename, bitrate
from common import TravelData




if __name__ == "__main__":
    params = get_bus_config(["socketcan"])
    params["bitrate"] = bitrate

    init_tee(can.Bus(**params))
    tm1 = create_device(node_id=1)
    tm2 = create_device(node_id=2)



    tm1.controller.idle()
    tm2.controller.idle()

