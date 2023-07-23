
import math
import can
import time
from tinymovr.tee import init_tee
from tinymovr.config import get_bus_config, create_device

import time
import datetime;
from datetime import datetime
import pickle
from params import pkl_filename


bitrate = 1000000
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

    maxCount = 50;

    transitions = [5, 16, maxCount+1]

    transitionIndex = 0



    maxTorque = 1.0

    currTorque = 0.0
    turn = 0
    prev = 0

    tm1.controller.current.Iq_setpoint=0
    tm1.controller.current_mode()

    tm2.controller.current.Iq_setpoint=0
    tm2.controller.current_mode()

    start_enc = tm2.encoder.position_estimate
    enc_rec = []
    for count in range(maxCount):
        if count >= transitions[transitionIndex]:
            turn = 1-turn
            transitionIndex += 1


        if (prev != turn):
            currTorque = turn*maxTorque
            tm1.controller.current.Iq_setpoint=currTorque
            tm2.controller.current.Iq_setpoint=currTorque
            print("count: %d torque: %f" % (count, currTorque) )

        enc = tm2.encoder.position_estimate
        enc_rec.append(enc)
        prev = turn
        ct = datetime.now()
        ts = ct.timestamp()
        #print("", end=" ")
        print(ts, end=": ")
        print(enc-start_enc)
        time.sleep(sleepTimeMs/1000.0)

    tm1.controller.idle()
    tm2.controller.idle()

    enc_rec = [item-start_enc for item in enc_rec]
    print(enc_rec)
    with open(pkl_filename, 'wb') as f:
        pickle.dump(enc_rec, f)
