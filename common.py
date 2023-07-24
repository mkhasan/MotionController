
class TravelData:
    def __init__(self, init_enc, transitions, max_torque):
        self.init_enc = init_enc
        self.ts = []
        self.enc =[]
        self.torque = []
        self.velocity = []
        self.transitions = transitions
        self.min_torque = 0.0
        self.max_torque = max_torque

    def append(self, ts, enc, velocity, torque ):
        self.ts.append(ts)
        self.enc.append(enc)
        self.torque.append(torque)
        self.velocity.append(velocity)
