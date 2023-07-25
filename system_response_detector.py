
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



#init_tee(can.Bus(**params))
#tm = create_device(node_id=1)

#tm.controller.calibrate()


sleepTimeMs = 100
if __name__ == "__main__":
    params = get_bus_config(["socketcan"])
    params["bitrate"] = bitrate

    init_tee(can.Bus(**params))
    tm1 = create_device(node_id=1)
    tm2 = create_device(node_id=2)

    maxCount = 100;

    transitions = [5, 20, 30, 40, 50, 65, 70, 80, 95, maxCount+1]

    torquePreset = [2.0, 2.5, 4.0, -2.5, 4.0, 2.5, -3.5, -2.0, 0.0, 0.0]

    transitionIndex = 0



    id = '0'
    if len(sys.argv) > 1:
        id = sys.argv[1]

    filename = "test_%s.pkl" % id

    maxTorque = 2.0

    currTorque = 0.0
    turn = 0
    prev = 0

    tm1.controller.current.Iq_setpoint=0
    tm1.controller.current_mode()

    tm2.controller.current.Iq_setpoint=0
    tm2.controller.current_mode()

    start_enc = tm1.encoder.position_estimate

    travelData = TravelData(float(start_enc.m), transitions, maxTorque)

    for count in range(maxCount):
        if count >= transitions[transitionIndex]:

            currTorque = torquePreset[transitionIndex]
            tm1.controller.current.Iq_setpoint=currTorque
            tm2.controller.current.Iq_setpoint=currTorque
            transitionIndex += 1
            print("count: %d torque: %f" % (count, currTorque) )


        enc = tm1.encoder.position_estimate
        vel = tm1.encoder.velocity_estimate


        ct = datetime.now()
        ts = ct.timestamp()

        travelData.append(ts, float(enc.m), float(vel.m), currTorque)
        #print("", end=" ")
        print(ts, end=": ")
        print(enc)
        time.sleep(sleepTimeMs/1000.0)

    tm1.controller.idle()
    tm2.controller.idle()



    with open(filename, 'wb') as f:
        pickle.dump(travelData, f)
        f.close()
        print("done")
