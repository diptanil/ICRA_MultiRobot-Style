class EventModel:

    def __init__(self, w, w0, p, g):
        self.states = w
        self.initial = w0
        self.transitionProb = p
        self.occurenceFn = g

    def get_nxt_states(self, st):
        transitions_st = self.transitionProb[self.states.index(st)]
        nxt_sts = []

        for ind, prob in enumerate(transitions_st):
            if prob > 0:
                nxt_sts.append((self.states[ind], prob))

        return nxt_sts

    def get_event_occurence_prob(self, st, evt):
        try:
            prob = self.occurenceFn[st][evt]
        except:
            prob = 0.0

        return prob

    def get_transition_probability(self, fw, tw):
        return self.transitionProb[self.states.index(fw)][self.states.index(tw)]