import math
import sys
import time
import datetime;
from datetime import datetime
import pickle
from params import pkl_filename

from common import TravelData
import pickle
from params import pkl_filename

import matplotlib.pyplot as plt
import numpy as np


from params import pkl_filename, bitrate

if __name__ == "__main__":

    basename = sys.argv[1]
    filename = basename + ".pkl"
    #travelData = TravelData(0, 0, 0)
    with open(filename, 'rb') as f:
        travelData = pickle.load(f)

    #print(travelData.torque)
    #print(travelData.ts)
    #print(travelData.enc)
    #print(travelData.init_enc)
    #print(travelData.transitions)

    initTime = travelData.ts[0]
    ts = [item-initTime for item in travelData.ts]
    t_gap = [1.0*(ts[k+1] - ts[k]) for k in range(len(ts)-1)]
    print(np.mean(t_gap))
    enc = [item - travelData.init_enc for item in travelData.enc]

    maxVal = np.max(travelData.velocity)
    print(maxVal)
    line = np.arange(len(ts))
    plt.plot(line, enc)

    plt.plot(line, [item * maxVal for item in travelData.torque])
    plt.show()

    attrs = ['torque', 'velocity', 'enc']
    values = [travelData.torque, travelData.velocity, enc]




    for atrr, value in zip(attrs, values):
        output_filename = "out_%s_%s.pkl" % (basename, atrr)
        with open(output_filename, "wb") as file:
            pickle.dump(value, file)






    
