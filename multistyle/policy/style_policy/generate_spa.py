from .utils.styleMDP import StyleMDP
from .utils.spa_st_act import SPA_st

import itertools

class SPA:

    def __init__(self, problem, jpg, o_robot):
        self.problem = problem
        self.jpg = jpg
        self.ordered_robots = o_robot
        self.MDP = StyleMDP()

        self.constructMDP()
        self.MDP.printMDP()
        self.MDP.optimalPolicy_InfiniteHorizon(self.problem.special_STOP,  isverbose = True, displaydelta = True, printpolicy = True, epsilonOfConvergence = 0.01, discount = 0.8)

    def st_in_list(self, st, list):
        for state in list:
            if st.is_equal(state):
                return True

        return False

    def style_from_eve_seq(self, e_seq):
        sty = []
        for ind, r in enumerate(self.ordered_robots):
            e = e_seq[ind]
            if e in [self.problem.special_DN, self.problem.special_unsucessful]:
                sty.append([self.problem.special_Blank])
            else:
                sty.append(self.problem.sc[r].catalogue[e])

        all_sty = list(itertools.product(*sty))
        return all_sty

    def constructMDP(self):
        sty = tuple()
        for i in range(self.problem.styGram.k - 1):
            sty = sty + tuple([self.problem.special_Blank])
        self.MDP.initial = SPA_st(self.jpg.start, sty)

        not_visited = [self.MDP.initial]
        visited = []

        while not_visited:
            state = not_visited.pop()
            visited.append(state)

            if not self.st_in_list(state, self.MDP.states):
                self.MDP.add_StyMDP_state(state)

            print(state.jpg_st.str_name)

            nxt_jpg_sts_prob = self.jpg.get_transition_from_st(state.jpg_st)

            edge_sty_choices = []

            for nxt_j_st_p in nxt_jpg_sts_prob:
                # print(f"{nxt_j_st_p[0]} {nxt_j_st_p[0].events} {nxt_j_st_p[1]}")
                # print(f"{self.style_from_eve_seq(nxt_j_st_p[0].events)}")
                edge_sty_choices.append(self.style_from_eve_seq(nxt_j_st_p[0].events))

            actions_state = list(itertools.product(*edge_sty_choices))
            # print(actions_state)

            for act in actions_state:
                for ind, sty in enumerate(act):
                    rew, sty_nxt = self.problem.styGram.get_transition_weight(state.style, sty)
                    # print(f"{rew} {sty} {sty_nxt} {nxt_jpg_sts_prob[ind][0]} {nxt_jpg_sts_prob[ind][1]}")
                    nxt_spa_st = SPA_st(nxt_jpg_sts_prob[ind][0], sty_nxt)
                    self.MDP.add_StyMDP_transition(state, act, nxt_spa_st, nxt_jpg_sts_prob[ind][1], rew)

                    if not self.st_in_list(nxt_spa_st, visited):
                        if not self.st_in_list(nxt_spa_st, not_visited):
                            not_visited.append(nxt_spa_st)


