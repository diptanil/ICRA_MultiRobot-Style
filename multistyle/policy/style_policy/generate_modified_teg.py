from .utils.modified_teg_st_act import MTEG_st
from ...utils.utils import UtilityFunctions
from .utils.fundamental_matrix import generate_b_matrix

import numpy as np

class ModifiedTEG:
    def __init__(self, problem, o_pol, o_robots):
        self.problem = problem
        self.ordered_epolicy = o_pol
        self.robots = o_robots

        self.states_a = []
        self.states_b = []

        self.edges_a = []
        self.edges_b = []

        self.start = None

        self.all_abs_sts = []

        self.final_transition = []
        self.final_transition_r = []
        self.final_transition_c = []

        self.generate_MTEG()

        # for st in self.states_a + self.states_b:
        #     print(str(st))
        #
        for edge in self.edges_a + self.edges_b:
            print(f"{edge[0]} -- {edge[2]} --> {edge[1]}  Prob {edge[3]}")



        teg_mat = self.generate_transitions()

        self.get_all_absorbing_sts(teg_mat)

        # print(teg_mat)
        # for st in self.all_abs_sts:
        #     print(st)

        self.get_absorbtion_prob(teg_mat)

        # print("\n\n\n")
        # print(f"{self.final_transition_c}")
        #
        # for ind, r in enumerate(self.final_transition_r):
        #     print(f"{r}  {self.final_transition[ind]}")

        # action = self.get_pol('w0', 'q1', ['v0', 'v0'])
        # events = self.get_evt_act(action)

    def get_pol(self, em_st, sa_st, V_sts):
        # print(f"{em_st}, {sa_st}, {V_sts}")
        action = tuple()
        nxt_v = tuple()
        o_n = len(self.robots)
        o_n_st = "(" + str(em_st) + ", " + str(sa_st) + ", " + str(V_sts[o_n-1]) + ")"
        o_n_pol = self.ordered_epolicy[o_n]['MDP'].policy[o_n_st]
        if o_n_pol == self.problem.special_STOP:
            return self.problem.special_STOP, tuple()
        o_n_act = self.ordered_epolicy[o_n]['MDP'].action_name_dic[o_n_pol]
        # print(f"Policy for the last calculated robot is {o_n_act}")
        for i in range(1, o_n):
            st_name = "(" + str(em_st) + ", " + str(sa_st) + ", " + str(V_sts[i-1]) + ")"
            pol = self.ordered_epolicy[i]['MDP'].policy[st_name]
            act = self.ordered_epolicy[i]['MDP'].action_name_dic[pol]
            # print(f"Action for robot in order {i} is {act}")
            if o_n_act.act_seq_dn[i-1] ==  self.problem.special_noAction:
                # action.append('NA')
                action = action + tuple([self.problem.special_noAction])
                nxt_vi_st, cos = self.problem.v[self.robots[i-1]].get_nxt_state_cost(V_sts[i-1], self.problem.special_noAction)
                nxt_v = nxt_v + tuple([nxt_vi_st])
            else:
                # action.append(act.self_action)
                action = action + tuple([act.self_action])
                nxt_vi_st, cos = self.problem.v[self.robots[i - 1]].get_nxt_state_cost(V_sts[i - 1], act.self_action)
                nxt_v = nxt_v + tuple([nxt_vi_st])

        # action.append(o_n_act.self_action)
        action = action + tuple([o_n_act.self_action])
        nxt_vi_st, cos = self.problem.v[self.robots[o_n - 1]].get_nxt_state_cost(V_sts[o_n - 1], o_n_act.self_action)
        nxt_v = nxt_v + tuple([nxt_vi_st])

        return action, nxt_v #, robot_ordr

    def get_evt_act(self, action, to_w):
        # events = tuple()
        e_set = set()
        for act in action:
            e = self.problem.recordingFn[act]
            # events = events + tuple([e])
            if e != self.problem.special_DN:
                e_set.add(e)

        ep = UtilityFunctions.powerset(e_set)

        valid_e_seq = {}

        for epi in ep:
            v_e = tuple()
            p_ve = 1.0

            for e in e_set:
                g_e = self.problem.event_model.get_event_occurence_prob(to_w, e)
                if e in epi:
                    p_ve = p_ve * g_e
                else:
                    p_ve = p_ve * (1 - g_e)

            for a in action:
                e = self.problem.recordingFn[a]
                if e in epi:
                    v_e = v_e + tuple([e])
                elif e == self.problem.special_DN:
                    v_e = v_e + tuple([self.problem.special_DN])
                else:
                    v_e = v_e + tuple([self.problem.special_unsucessful])

            valid_e_seq[v_e] = p_ve

        return valid_e_seq

    def unsucessful_transition(self, evnt_seq):
        for e in evnt_seq:
            if e not in [self.problem.special_DN, self.problem.special_unsucessful]:
                return False

        return True

    def st_in_list(self, st, list):
        for state in list:
            if st.is_equal(state):
                return True

        return False

    def get_st_ind_in_list(self, st, list):
        for ind, state in enumerate(list):
            if st.is_equal(state):
                return ind

    def generate_MTEG(self):

        start_v_st = tuple()
        for r in self.robots:
            start_v_st = start_v_st + tuple([self.problem.v[r].initial])

        self.start = MTEG_st(self.problem.event_model.initial, "", self.problem.story.initial, start_v_st)

        self.states_a = [self.start]

        visited = []
        not_visited = [self.start]

        while not_visited:
            state = not_visited.pop()

            if not self.st_in_list(state, visited):
                visited.append(state)
            if not self.st_in_list(state, self.states_a):
                self.states_a.append(state)

            nxt_em_states = self.problem.event_model.get_nxt_states(state.em_st)
            act, nxt_v_sts = self.get_pol(state.em_st, state.sa_st, state.v_sts)

            if act == self.problem.special_STOP:
                continue

            for nxt_em_st in nxt_em_states:
                evt_seqs = self.get_evt_act(act, nxt_em_st[0])
                for e_seq in list(evt_seqs.keys()):
                    if not self.unsucessful_transition(e_seq) and evt_seqs[e_seq] > 0.0:
                        nxt_sa_st = self.problem.story.get_state_reachable(state.sa_st, e_seq)
                        nxt_st = MTEG_st(nxt_em_st[0], e_seq, nxt_sa_st, nxt_v_sts)
                        nxt_st_temp = MTEG_st(nxt_em_st[0], "", nxt_sa_st, nxt_v_sts)
                        self.edges_b.append([state, nxt_st, e_seq, nxt_em_st[1]*evt_seqs[e_seq]])
                        if not self.st_in_list(nxt_st, self.states_b):
                            self.states_b.append(nxt_st)
                            self.edges_a.append([nxt_st, nxt_st, '', 1.0])
                        if not self.st_in_list(nxt_st, visited):
                            if not self.st_in_list(nxt_st, not_visited):
                                not_visited.append(nxt_st_temp)

                    elif evt_seqs[e_seq] > 0.0:
                        nxt_st = MTEG_st(nxt_em_st[0], "", state.sa_st, nxt_v_sts)
                        self.edges_a.append([state, nxt_st, e_seq, nxt_em_st[1]])
                        if not self.st_in_list(nxt_st, self.states_a):
                            self.states_a.append(nxt_st)
                        if not self.st_in_list(nxt_st, visited):
                            if not self.st_in_list(nxt_st, not_visited):
                                not_visited.append(nxt_st)

    def generate_transitions(self):
        states = np.array(self.states_a + self.states_b)
        mat = np.array([[0.0 for i in range(len(states))] for j in range(len(states))])

        for edge in self.edges_a:
            r = self.get_st_ind_in_list(edge[0], states)
            c = self.get_st_ind_in_list(edge[1], states)

            mat[r][c] = mat[r][c] + edge[3]

        for edge in self.edges_b:
            r = self.get_st_ind_in_list(edge[0], states)
            c = self.get_st_ind_in_list(edge[1], states)

            mat[r][c] = mat[r][c] + edge[3]

        return mat

    def get_all_absorbing_sts(self, mat):
        states = np.array(self.states_a + self.states_b)

        for ind, state in enumerate(states):
            if 1.0 in mat[ind]:
                self.all_abs_sts.append(state)

    def get_absorbtion_prob(self, mat):
        # states = np.array(self.states_a + self.states_b)
        states = []
        for st in self.states_a + self.states_b:
            states.append(str(st))
        abs_sts = []
        for ab_st in self.all_abs_sts:
            abs_sts.append(str(ab_st))
        self.final_transition, self.final_transition_r, self.final_transition_c = generate_b_matrix(mat, states, abs_sts)

    def get_abs_prob_frmst_tost(self, from_st, to_st):

        try:
            prob = self.final_transition[self.final_transition_r.index(str(from_st))][self.final_transition_c.index(str(to_st))]
        except:
            prob = 0.0

        return prob






