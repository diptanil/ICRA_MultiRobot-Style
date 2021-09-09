class ValidActionAutomata:
    def __init__(self, n, v, v0, a, tc, nac=0):
        self.type = n
        self.states = v
        self.initial = v0
        self.actions = a
        self.validTransitionCostDic = tc
        self.noActionCost = nac

    def get_valid_actions(self, st):
        return list(self.validTransitionCostDic[st].keys())

    def get_nxt_state_cost(self, st, a):
        state = self.validTransitionCostDic[st][a][0]
        cost = self.validTransitionCostDic[st][a][1]

        return state, cost