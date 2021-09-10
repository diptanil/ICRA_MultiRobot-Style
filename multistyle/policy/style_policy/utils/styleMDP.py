from sys import float_info

import time
import math

class StyleMDP:
    def __init__(self):
        self.states = []
        self.initial = None
        self.tranProbCost = {}
        self.final = []
        self.state_names = {}

        self.special_STOP = None

        self.action_name_dic = {}

        self.time_to_compute = None
        self.policy = None
        self.U = None

    def add_StyMDP_state(self, state):

        for st in self.states:
            if state.is_equal(st):
                print(f"ERROR : State {state} already exists")
                return False
        self.states.append(state)
        self.state_names[state.str_name] = state
        if state not in self.final:
            self.tranProbCost[state.str_name] = {}
        return True

    def add_StyMDP_transition(self, from_st, act, to_st, prob, cost):

        if from_st.str_name not in list(self.tranProbCost.keys()):
            print(f"Error: from state {from_st} not found during adding transition")
            return False

        if str(act) not in list(self.tranProbCost[from_st.str_name].keys()):
            self.tranProbCost[from_st.str_name][str(act)] = {}
            self.action_name_dic[str(act)] = act
        if to_st.str_name not in list(self.tranProbCost[from_st.str_name][str(act)].keys()):
            self.tranProbCost[from_st.str_name][str(act)][to_st.str_name] = [prob, cost]
        else:
            self.tranProbCost[from_st.str_name][str(act)][to_st.str_name][0] += prob # Probability update
            # self.tranProbCost[from_st.str_name][str(act)][to_st.str_name][1] = \
            #     self.tranProbCost[from_st.str_name][str(act)][to_st.str_name][1] + cost# Cost update
        # print(f"\nAdded {from_st.str_name} -- {str(act)} --> {to_st.str_name}. Prob {prob} Cost {cost}.")
        return True

    def in_final(self, state):
        for s_f in self.final:
            if state.is_equal(s_f):
                return True
        return False

    def optimalPolicy_InfiniteHorizon(self, sp_stop,  isverbose, displaydelta, printpolicy, epsilonOfConvergence = 0.01, discount = 0.8):
        self.special_STOP = sp_stop
        if isverbose:
            print("Computing the optimal policy")

        start_time = time.time()

        u1 = {}
        pi = {}

        for state in self.states:
            u1[state.str_name] = 0
            pi[state.str_name] = ""

        i = 0
        # end_loop = False
        while True:
            u = u1.copy()
            delta = 0

            for j, s in enumerate(self.states):
                # for s_f in self.final:
                #     if s.is_equal(s_f):
                #         pi[s.str_name] = self.special_STOP
                #         # u1[s.str_name] = 0
                #         # u[s.str_name] = 0
                #         continue
                if self.in_final(s):
                    pi[s.str_name] = self.special_STOP
                    u1[s.str_name] = 0.0
                    u[s.str_name] = 0.0
                    continue
                max_val = - math.inf
                for action in list(self.tranProbCost[s.str_name].keys()):
                    val = 0.0
                    # if s not in self.final:
                    # val += 10
                    # if not self.in_final(s):
                    #     val += 10
                    for nxt in list(self.tranProbCost[s.str_name][action].keys()):
                        #logger.debug(nxt)
                        # val = val + self.tranProbCost[s[3]][action][nxt][1] + \
                        # self.tranProbCost[s[3]][action][nxt][0] * u1[nxt]
                        val = val + self.tranProbCost[s.str_name][action][nxt][0] * (self.tranProbCost[s.str_name][action][nxt][1] + discount*u[nxt])
                        # print(
                        #     f"{s.str_name} {action} {nxt} {self.tranProbCost[s.str_name][action][nxt][0]}"
                        #     f" {self.tranProbCost[s.str_name][action][nxt][1]} {val}")
                        #logger.debug(val)
                    # print(f"State {s.str_name} Action {action} Minval = {min_val} val = {val}")
                    if val > max_val:
                        pi[s.str_name] = action
                        max_val = val

                # if s.is_equal(self.initial):
                #     delta = abs(max_val - u[self.initial.str_name])

                u1[s.str_name] = max_val
                #delta = max(delta, abs(u1[s[3]] - u[s[3]]))

                if delta < abs(u1[s.str_name] - u[s.str_name]):
                    delta = abs(u1[s.str_name] - u[s.str_name])

                if displaydelta:
                    print(f"Delta={delta}")

            if delta < epsilonOfConvergence * (1 - discount) / discount:
                end_time = time.time()
                self.time_to_compute = end_time - start_time
                self.expected_cost = u1[self.initial.str_name]
                # if isverbose:
                #     print(f"Expected cost to reach a goal state: {self.expected_cost}\n\n"
                #           f"Time to compute optimal policy {self.time_to_compute}")
                self.policy = pi
                self.U = u1
                if printpolicy:
                    self.printpolicy()
                return pi

            i += 1
            end_loop = True

    def optimalPolicy_FiniteHorizon(self, sp_stop,  isverbose, printpolicy, k = 50):
        self.special_STOP = sp_stop

        start_time = time.time()

        u1 = dict([(s.str_name, 0) for s in self.states])
        pi = dict([(s.str_name, "") for s in self.states])

        for state in self.states:
            for s_f in self.final:
                if state.is_equal(s_f):
                    pi[state.str_name] = self.special_STOP

        for i in range(k-1, -1, -1):
            u = u1.copy()
            if isverbose:
                print(f"Iteration {i+1}")

            n = 1
            for j,s in enumerate(self.states):
                n+=1
                for s_f in self.final:
                    if s.is_equal(s_f):
                        pi[s.str_name] = self.special_STOP
                        u1[s.str_name] = 0.0
                        continue

                min_val = float_info.max
                optAct = ""

                for action in list(self.tranProbCost[s.str_name].keys()):
                    val = 0.0
                    for nxt in list(self.tranProbCost[s.str_name][action].keys()):
                        val = val + self.tranProbCost[s.str_name][action][nxt][0]* (self.tranProbCost[s.str_name][action][nxt][0] + u[nxt])

                    if val < min_val:
                        min_val = val
                        optAct = action

                u1[s.str_name] = min_val
                pi[s.str_name] = optAct

        end_time = time.time()
        self.time_to_compute = end_time - start_time
        self.policy = pi
        self.U = u1
        if printpolicy:
            self.printpolicy()
        self.expected_cost = u1[self.initial.str_name]

        return pi


    def get_action_cost_forSeqMDP(self, va_st, act_str):

        act = self.action_name_dic[act_str].self_action
        st, cost = self.vr.get_nxt_state_cost(va_st, act)

        return act, cost


    def get_policy_for_seqMDP(self, em_st, sa_st):
        act = []
        max_cost = 0.0
        count = 0
        for st in self.states:
            if st.em_state == em_st and st.sa_state == sa_st:
                act_pol = self.policy[st.str_name]
                count += 1
                if act_pol != self.special_STOP:
                    pol, cost = self.get_action_cost_forSeqMDP(st.va_state, act_pol)
                    act.append(pol)
                    if max_cost <= cost:
                        max_cost = cost
                else:
                    act.append(self.special_STOP)

        prob = 1/count
        return act, prob, max_cost

    def printpolicy(self):

        print(f"\n\nPrinting policy\n")

        for state in self.states:
            st_nam = state.str_name
            pol = self.policy[state.str_name]
            act = ''
            if pol != "":
                act = self.action_name_dic[pol] # .self_action
                print(f"State {st_nam} --> Policy : {pol} ||| Next states {list(self.tranProbCost[st_nam][pol].keys())}")
            else:
                print(
                    f"State {st_nam} --> Policy : {pol}")
                  # f"(Action : {act})")
                  # f"--> Expected Cost {self.U[state.str_name]}")

    def printMDP(self):
        for state in self.states:
            for action in list(self.tranProbCost[state.str_name].keys()):
                for nxt_st in list(self.tranProbCost[state.str_name][action].keys()):
                    print(f"{state.str_name} -- {action} ->  {nxt_st}"
                          f"prob {self.tranProbCost[state.str_name][action][nxt_st][0]} and cost{self.tranProbCost[state.str_name][action][nxt_st][1]}")

    def get_noActionCost(self):
        return self.vr.noActionCost