
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


sleepTimeMs = 10

ct = datetime.now()
prev = ct.timestamp()

P_gain = 2.389411601e-5
I_gain = 0.0090678223466725

proportionalError = 0.0;
integralError = 0.0

maxCount = 1000

transitions = [50, 200, 600, maxCount+1]
velocities = [20000.0, 30000, 0, 0]


assert (len(transitions) == len(velocities))

max_error = 50000.0
max_integral_error = 50000
max_u = 3.0;
if __name__ == "__main__":
    params = get_bus_config(["socketcan"])
    params["bitrate"] = bitrate
    init_tee(can.Bus(**params))
    tm1 = create_device(node_id=1)
    tm2 = create_device(node_id=2)

    tm1.controller.current.Iq_setpoint=0
    tm1.controller.current_mode()

    tm2.controller.current.Iq_setpoint=0
    tm2.controller.current_mode()

    count = 0;
    transitionIndex = 0
    error = 0.0
    vel = 0.0
    target = 0.0
    u = 0.0
    while(count < maxCount):

        vel = tm1.encoder.velocity_estimate

        error = target-float(vel.m)
        if (math.fabs(error) > max_error or integralError > max_integral_error):
            print(("Error exceedddddded (%lf %lf)!!!" % (error, integralError)));
        else:
            proportionalError = error;
            integralError += error;
            u = P_gain*proportionalError+I_gain*integralError
            if (math.fabs(u) < max_u):
                tm1.controller.current.Iq_setpoint=u
                tm2.controller.current.Iq_setpoint=u
                pass
            else:
                print("input too high vel: %lf u: %lf error: %lf integral error: %lf" % ( float(vel.m), u, error, integralError))

        if count > transitions[transitionIndex]:
            target = velocities[transitionIndex]
            transitionIndex += 1



        print("count: %d curr velocity: %lf integral error: %lf target: %lf u: %lf" % (count, float(vel.m), integralError, target, u))
        ct = datetime.now()
        ts = ct.timestamp()
        #print("val: %lf" % 3.4e-2)

        prev = ts

        count += 1

        time.sleep(sleepTimeMs/1000.0)


    tm1.controller.idle()
    tm2.controller.idle()
