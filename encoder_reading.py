import math
import can
import time
from tinymovr.tee import init_tee
from tinymovr.config import get_bus_config, create_device

import time
import datetime;
from datetime import datetime
import pickle
from params import pkl_filename, bitrate

import pint
from decimal import Decimal as D
import decimal

#init_tee(can.Bus(**params))
#tm = create_device(node_id=1)

#tm.controller.calibrate()

pkl_filename1 = "data1.pkl"

sleepTimeMs = 100
if __name__ == "__main__":
    params = get_bus_config(["socketcan"])
    params["bitrate"] = bitrate

    init_tee(can.Bus(**params))
    tm1 = create_device(node_id=1)
    tm2 = create_device(node_id=2)


    tm1.controller.idle()
    tm2.controller.idle()


    start_enc = tm1.encoder.position_estimate


    start_enc = start_enc.m
    #print(type(start_enc))

    ct = datetime.now()
    ts = ct.timestamp()
    #print(type(ts))

    val = tm1.encoder.velocity_estimate
    print(type(val.m))

    with open(pkl_filename1, "wb") as f:
        pickle.dump(start_enc, f)

    with open(pkl_filename1, "rb") as f:
        test = pickle.load(f)
        #print(test)


