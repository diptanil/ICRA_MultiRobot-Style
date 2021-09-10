import math

class StyleBiGram:
    def __init__(self, g, g0, k, sig, om):
        self.states = g
        self.initial = g0
        self.k = k
        self.special_Blank = sig
        self.weights = om

    def get_transition_weight(self, old_sty, sty_seq):
        reward = 0.0
        old = old_sty
        for sty in sty_seq:
            print(f"{old}  {sty}")
            if sty != self.special_Blank:
                try:
                    w = self.weights[sty][old]
                except:
                    w = 0.0
                if w > 0.0:
                    reward = reward + math.log(w)
                else:
                    reward = reward -1000.0

                old = sty

        return reward, old
