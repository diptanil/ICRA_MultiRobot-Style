class StoryAutomata:

    def __init__(self, q, q0, d, evt, acc, evt_DN):

        self.states = q
        self.initial = q0
        self.transitions = d
        self.events = evt
        self.accepting = acc
        self.special_DN = evt_DN

    def get_nxt_transition(self, q, e):
        try:
            nxt_st = self.transitions[q][e]
        except:
            nxt_st = None
        return  nxt_st

    def get_evts_outgoing(self, q):
        return set(self.transitions[q])

    def get_state_reachable(self, q,  evt_seq):
        state = q
        for e in evt_seq:
            if e == self.special_DN:
                continue
            try:
                nxt_st = self.transitions[state][e]
            except:
                nxt_st = state
            state = nxt_st

        return state
