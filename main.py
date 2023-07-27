
import math
import can
from tinymovr.tee import init_tee
from tinymovr.config import get_bus_config, create_device

import time
from datetime import datetime

bitrate = 1000000
#init_tee(can.Bus(**params))
#tm = create_device(node_id=1)

#tm.controller.calibrate()


if __name__ == "__main__":
    params = get_bus_config(["socketcan"])
    params["bitrate"] = bitrate

    print(params)


    init_tee(can.Bus(**params))
    tm1 = create_device(node_id=1)
    tm2 = create_device(node_id=2)

    MAX_VELOCITY = 150000
    velocity = 20000
    step = 10000;

    both = False;

    while True:
        inp = input("Enter your choise (s: single, d: double, g: go, 't' stop, '+' inc, '-' dec, 'x' exit, abs(val) > 500: valocity) ")

        if (inp == 'x'):
            exit(1)

        if (inp == 's'):
            both = False
            continue

        if (inp == 'd'):
            both = True
            continue

        if (inp == "g"):


            tm2.controller.velocity.setpoint = velocity
            tm2.controller.velocity_mode()

            if both == True:
                tm1.controller.velocity.setpoint = velocity
                tm1.controller.velocity_mode()

            continue



        if (inp == 't'):
            tm2.controller.idle()
            tm1.controller.idle()
            continue

        if (inp == '+'):
            velocity += step
            tm2.controller.velocity.setpoint = velocity;
            #tm2.controller.velocity_mode()
            continue;

        if (inp == '-'):
            velocity -= step
            tm2.controller.velocity.setpoint = velocity;
            continue;


        try:
            val = int(inp)
        except:
            print("Invalid input")
            val = 0

        finally:
            if abs(val) >= 500 and abs(val) < MAX_VELOCITY:
                print("Setting velocity to %d" % val )
                velocity = val;

