
import math
import sys
import _thread

import can
import time
from tinymovr.tee import init_tee
from tinymovr.config import get_bus_config, create_device

import time
import datetime;
from datetime import datetime
import pickle
from params import pkl_filename, bitrate
from common import TravelData, StreamingMovingAverage
from cmd_handler import CmdHandler



#init_tee(can.Bus(**params))
#tm = create_device(node_id=1)

#tm.controller.calibrate()


sleepTimeMs = 1

ct = datetime.now()
prev = ct.timestamp()

P_gain = 2.389411601e-5
#I_gain = 0.00906782
I_gain = 0.0001

proportionalError = 0.0;
integralError = 0.0

maxCount = 2000

#transitions = [50, 1500, 1800, maxCount+1]
#velocities = [20000.0, 16000, 0, 0]

transitions = [50, 1500, 1800, maxCount+1]
velocities = [25000.0, 18000, 0, 0]


assert (len(transitions) == len(velocities))

max_error = 50000.0
max_integral_error = 50000
max_u = 6.0;

min_velocity = 10000.0
max_velocity = 50000.0

streamingMovingAverage = StreamingMovingAverage(10)

dir = 1;
quit = False
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "back":
        dir = -1

    for i in range(len(velocities)):
        velocities[i] = velocities[i]*dir

    params = get_bus_config(["socketcan"])
    params["bitrate"] = bitrate
    init_tee(can.Bus(**params))
    tm1 = create_device(node_id=1)
    tm2 = create_device(node_id=2)

    tm1.controller.current.Iq_setpoint=0
    tm1.controller.current_mode()

    tm2.controller.current.Iq_setpoint=0
    tm2.controller.current_mode()


    lock=_thread.allocate_lock()
    cmdHandler = CmdHandler(lock, min_velocity-10.0)

    while(quit == False):
        count = 0;
        transitionIndex = 0
        error = 0.0
        vel = 0.0
        target = 0.0
        u = 0.0
        while(count < maxCount and quit == False):
            dir = 1 if target >= min_velocity else -1
            if (dir > 0):
                currVelocity = tm2.encoder.velocity_estimate
            else:
                currVelocity = tm1.encoder.velocity_estimate

            #vel = streamingMovingAverage.process(float(currVelocity.m))
            vel = currVelocity.m

            error = target-vel
            if (math.fabs(error) > max_error or integralError > max_integral_error):
                print(("Error exceedddddded (%lf %lf)!!!" % (error, integralError)));
            else:
                proportionalError = error;
                integralError += (error*0.0035);
                u = P_gain*proportionalError+I_gain*integralError
                if (math.fabs(u) < max_u):
                    tm1.controller.current.Iq_setpoint=u
                    tm2.controller.current.Iq_setpoint=u
                    pass
                else:
                    print("input too high vel: %lf u: %lf error: %lf integral error: %lf" % ( float(vel), u, error, integralError))

            #if count > transitions[transitionIndex]:
            #    target = velocities[transitionIndex]
            #    transitionIndex += 1


            ct = datetime.now()
            ts = ct.timestamp()

            print(ts-prev, end=" - ")
            print("count: %d curr velocity: %lf integral error: %lf target: %lf u: %lf" % (count, float(vel), integralError, target, u))
            #print("val: %lf" % 3.4e-2)

            prev = ts

            count += 1

            value = cmdHandler.GetValue()

            if (value < 0.5):
                target = 0.0
            elif value >= min_velocity and value <= max_velocity:
                target = value

            time.sleep(sleepTimeMs/1000.0)


    tm1.controller.idle()
    tm2.controller.idle()
