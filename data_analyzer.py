import sys
from common import Trajectory

import matplotlib.pyplot as plt
import numpy as np

filename = "front1.txt"
if __name__ == "__main__":

    trajectory = Trajectory()
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as f:
        lines = f.readlines()

    ts = 0.0
    for line in lines:

        splitted = line.split()
        #print(splitted[0])

        if lines.index(line) > 0:
            ts += float(splitted[0])

        curr_v = float(splitted[6])
        target_v = float(splitted[-3])
        u = float(splitted[-1])

        trajectory.Set(ts, curr_v, target_v, u)

    gaps = [trajectory.ts[k+1]-trajectory.ts[k] for k in range(len(trajectory.ts)-1)]

    plt.plot(trajectory.ts, trajectory.curr_v)
    plt.plot(trajectory.ts, trajectory.target_v)
    print(len(gaps))
    plt.show()
