import random

class PseudoDirector:

    def __init__(self, sim_time):

        self.num_robot = 3
        self.event_list = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']
        self.world_states = ['w0', 'wa', 'wb', 'wc', 'wd', 'we', 'wf']
        self.world_initial = 'w0'

        # Special event for Do-Nothing - 'DN'
        self.special_DN = 'DN'

        # Special event for Stop Simulation (Successful capture of story) - 'STOP'
        self.special_end = 'STOP'

        #Define style Catalogue

        self.sty_cat = {}

        # Define style catalogue for robot type 1
        self.sty_cat[1] = {}
        self.sty_cat[1]['e1'] = ['s1', 's2', 's3']
        self.sty_cat[1]['e2'] = ['s1', 's3']
        self.sty_cat[1]['e3'] = ['s1', 's2']
        self.sty_cat[1]['e4'] = ['s1']
        self.sty_cat[1]['e5'] = ['s1', 's3']
        self.sty_cat[1]['e6'] = ['s1', 's2', 's3']

        # Define style catalogue for robot type 2
        self.sty_cat[2] = {}
        self.sty_cat[2]['e1'] = ['s1']
        self.sty_cat[2]['e2'] = ['s1', 's2']
        self.sty_cat[2]['e3'] = ['s1', 's3']
        self.sty_cat[2]['e4'] = ['s2', 's3']
        self.sty_cat[2]['e5'] = ['s1', 's3']
        self.sty_cat[2]['e6'] = ['s1', 's2', 's3']

        # Define style catalogue for robot type 3
        self.sty_cat[3] = {}
        self.sty_cat[3]['e1'] = ['s2', 's3']
        self.sty_cat[3]['e2'] = ['s1']
        self.sty_cat[3]['e3'] = ['s1', 's3']
        self.sty_cat[3]['e4'] = ['s3']
        self.sty_cat[3]['e5'] = ['s3']
        self.sty_cat[3]['e6'] = ['s1', 's3']

        print(f"Running Pseudo-Director code for {self.num_robot} robots")

        # Since pseudo diretor does not have any story automaton
        # the code will run for tot steps then will give STOP

        self.tot = sim_time
        self.simulation_t = 0

        self.capture_list = []




    def update(self, w_st, success):

        if len(success) == self.num_robot:

            self.simulation_t += 1

            old_capture = self.capture_list
            self.capture_list = []

            if self.simulation_t > self.tot:
                for r in range(self.num_robot):
                    self.capture_list.append((r+1, 'STOP', ''))

            elif w_st == self.world_initial and self.simulation_t == 1:
                for r in range(self.num_robot):
                    self.capture_list.append((r+1, 'DN', ''))

            else:
                for r in range(self.num_robot):
                    e_cap = random.choice(self.event_list + [self.special_DN])
                    if e_cap == self.special_DN:
                        sty_cap = ''
                    else:
                        sty_cap = random.choice(self.sty_cat[r+1][e_cap])
                    self.capture_list.append((r+1, e_cap, sty_cap))

            return self.capture_list

