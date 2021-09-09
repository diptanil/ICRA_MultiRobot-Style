import  numpy as np

class JPG:
    def __init__(self, problem, mod_teg):
        self.problem = problem
        self.mod_teg = mod_teg

        self.start = mod_teg.start
        self.states = [self.start] + mod_teg.states_b

        self.transitions = []
        self.generate_jpg()
        self.normalize_transitions()

        # for st in self.mod_teg.states_a:
        #     print(st)
        #
        for st in self.states:
            print(st)

        print(self.transitions)

    def generate_jpg(self):
        self.transitions = np.array([[0.0 for i in range(len(self.states))] for j in range(len(self.states))])

        for row_ind, row in enumerate(self.states):
            for col_ind, col in enumerate(self.states):
                if row.sa_st not in self.problem.story.accepting:
                    self.transitions[row_ind][col_ind] = self.mod_teg.get_abs_prob_frmst_tost(row.str_wo_evt(), str(col))

    def normalize_transitions(self):

        for row_ind, row in enumerate(self.transitions):
            sum = 0.0
            for val in row:
                sum = sum + val

            if sum > 0.0:
                for col_ind, val in enumerate(row):
                    self.transitions[row_ind][col_ind] = self.transitions[row_ind][col_ind]/sum

    def get_transition_from_st(self, state):
        state_transition = self.transitions[self.states.index(state)]
        # print(state_transition)

        res = []

        for ind, val in enumerate(state_transition):
            if val > 0.0:
                res.append([self.states[ind], val])

        return res
