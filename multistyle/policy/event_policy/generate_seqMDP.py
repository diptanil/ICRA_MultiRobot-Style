from ...utils.mdp import MDP
from .utils.smdp_state import SeqMDPState, SeqMDPAction
from ...utils.utils import UtilityFunctions

import time
import itertools

class SeqMDP:
    def __init__(self, problem, robot, order, prv_pols, verbose):
        self.problem = problem
        self.robot = robot
        self.order = order
        self.vr = self.problem.v[self.robot]
        self.prev_pols = prv_pols

        if verbose:
            print(f"\nCreating Sequential MDP for robot {self.robot} in order "
                  f"{self.order}")

            start_time = time.time() # Keeping track of time only if verbose

        self.construct_MDP()
        # self.MDP.printMDP()

        if verbose:
            end_time = time.time() # Keeping track of time only if verbose
            self.time_to_compute = end_time - start_time # Keeping track of time only if verbose
            print(f"\nSequential MDP created in {self.time_to_compute} secs.")

    def is_final_st(self, st):
        if st.sa_state in self.problem.story.accepting:
            return True
        else:
            return False

    def get_act_seq_from_prev(self, w_st, s_st, act, a_cost):
        # print(f"In get act seq")
        a_seq = []
        prob = 1.0
        act_cost = a_cost
        for o in range(self.order - 1):
            b_noAct = act[o] == self.problem.special_noAction
            if b_noAct:
                # print(f"No Action")
                a_seq.append([self.problem.special_noAction])
                prob = prob * 1.0
                act_cost = act_cost + self.prev_pols[o].get_noActionCost()
            else:
                a_s, ap, ac = self.prev_pols[o].get_policy_for_seqMDP(w_st, s_st)
                # print(f"Action {a_s} with cost {ac}")
                a_seq.append(a_s)
                prob = prob * ap
                act_cost = act_cost + ac

        a_seq.append([act[self.order-1]])

        act_list = list(itertools.product(*a_seq))

        return act_list, prob, act_cost

    def events_action(self, act, to_w):

        evnts = []
        e_set = set()
        for a in act:
            e = self.problem.recordingFn[a]
            evnts.append(e)
            if e!= self.problem.special_DN:
                e_set.add(e)

        ep = UtilityFunctions.powerset(e_set)
        # This power set looks over all the possibilities in which the world can evolve

        valid_e = {}

        for epi in ep:
            v_e = ()
            p_ve = 1.0
            for e in e_set:
                g_e = self.problem.event_model.get_event_occurence_prob(to_w, e)
                if e in epi:
                    p_ve = p_ve * g_e
                else:
                    p_ve = p_ve * (1 - g_e)
            for a in act:
                e = self.problem.recordingFn[a]
                if e in epi:
                    v_e = v_e + tuple([e])
                else:
                    v_e = v_e + tuple([self.problem.special_DN])

            valid_e[v_e] = p_ve

        return  valid_e

    def valid_evtseq_act(self, act_seq, from_w, to_w, act_p, tot_cost):
        valid_e_a = []
        # tot_cost = 0.0
        transP = self.problem.event_model.get_transition_probability(from_w, to_w)

        for act in act_seq:

            evt_act_p = self.events_action(act, to_w)

            evt_act = list(evt_act_p.keys())

            for ea_seq in evt_act:
                valid_e_a.append([ea_seq, act_p*transP*evt_act_p[ea_seq], tot_cost])

        return valid_e_a


    def construct_MDP(self):
        self.MDP = MDP()
        self.MDP.vr = self.vr
        print(f"Initial state {self.problem.v[self.robot].initial}")
        self.MDP.initial = SeqMDPState(self.problem.event_model.initial, self.problem.story.initial, self.vr.initial)

        for em_st in self.problem.event_model.states:
            for sa_st in self.problem.story.states:
                for v_st in self.vr.states:
                    new_st = SeqMDPState(em_st, sa_st, v_st)
                    self.MDP.add_SeqMDP_state(new_st)

        for state in self.MDP.states:

            if self.is_final_st(state):
                self.MDP.final.append(state)
                continue

            act_available = self.vr.get_valid_actions(state.va_state)

            nxt_w_sts = self.problem.event_model.get_nxt_states(state.em_state)
            # The next em states are received as a list of (state, prob) values

            for nxt_w in nxt_w_sts:
                for act in act_available:
                    # Each act is an action symbol
                    # if there are prev 2 robots (current order 3) the choices might be
                    # (, , a), (DN, ,a), (, DN, a), (DN, DN, a)
                    act_bn = list(itertools.combinations_with_replacement(["", self.problem.special_noAction], self.order-1))
                    acts_w_bn = [SeqMDPAction((*x, act)) for x in act_bn]
                    nxt_v, cost = self.vr.get_nxt_state_cost(state.va_state, act)

                    for abn_st in acts_w_bn:
                        abn = abn_st.act_seq_dn
                        act_seqs, a_seq_p, act_cost = self.get_act_seq_from_prev(state.em_state, state.sa_state, abn, cost)

                        e_seq = self.valid_evtseq_act(act_seqs, state.em_state, nxt_w[0], a_seq_p, act_cost)
                        # e_seq is a list of elements [possible event sequence from action, probability, cost]

                        for e_s in e_seq:
                            # e_s[0] - Possible event sequence
                            # e_s[1] - Probability
                            # e_s[2] cost of taking the action
                            nxt_sa_st = self.problem.story.get_state_reachable(state.sa_state, e_s[0])

                            to_state = SeqMDPState(nxt_w[0], nxt_sa_st, nxt_v)

                            self.MDP.add_SeqMDP_transition(state, abn_st, to_state, e_s[1], e_s[2])







