from ..utils.storyAutomata import StoryAutomata
from ..utils.eventModel import EventModel
from ..utils.validActionAutomata import ValidActionAutomata
from ..utils.styleCatalogue import StyleCatalogue
from ..utils.styleBigram import StyleBiGram

class CaseStudy1_Race2Robots:

    def __init__(self):

        self.description = "\n\n****************************************\n\n" \
                           "Case Study 1: \n" \
                           "Event Model - Race Simulation\n" \
                           "2 Different robots."

        self.num_robots = 2

        self.events = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']

        self.story = None
        self.event_model = None

        self.special_DN = 'DN' # Special event for do nothing.
        self.special_unsucessful = 'UN'

        self.initialize_story()
        self.initialize_eventModel()

        self.special_STOP = 'STOP'

        self.special_noAction = 'NA' # Special action - no action

        self.motionActions = ['lo']

        # Keep in the same order as that of the events
        self.recordActions = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']

        self.actions = self.motionActions + self.recordActions + [self.special_noAction]

        self.recordingFn = {}

        for a in self.motionActions:
            self.recordingFn[a] = self.special_DN

        for ind, act in enumerate(self.recordActions):
            self.recordingFn[act] = self.events[ind]

        self.recordingFn[self.special_noAction] = self.special_DN

        self.styles = ['s1', 's2', 's3', 's4', 's5']
        self.special_Blank = 'BK'

        self.styGram = None

        self.initialize_styGram()



        self.v1 = None
        self.v2 = None


        self.sc1 = None
        self.sc2 = None

        self.initialize_v1andsc1()
        self.initialize_v2andsc2()

        self.v = {}
        self.v['R1'] = self.v1
        self.v['R2'] = self.v2

        self.sc = {}
        self.sc['R1'] = self.sc1
        self.sc['R2'] = self.sc2

    # Initializing the Story Automaton
    def initialize_story(self):
        # sa_states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
        sa_states = ['q0', 'q1', 'q2', 'q5']
        sa_start_state = 'q0'

        sa_final_st = ['q5']

        sa_transition = {}
        sa_transition['q0'] = {}
        sa_transition['q0']['e1'] = 'q1'
        sa_transition['q0']['e2'] = 'q2'
        # sa_transition['q0']['e5'] = 'q3'
        sa_transition['q1'] = {}
        sa_transition['q1']['e5'] = 'q5'
        sa_transition['q2'] = {}
        sa_transition['q2']['e6'] = 'q5'
        # sa_transition['q3'] = {}
        # sa_transition['q3']['e6'] = 'q4'
        # sa_transition['q4'] = {}
        # sa_transition['q4']['e3'] = 'q5'
        # sa_transition['q4']['e4'] = 'q5'
        sa_transition['q5'] = {}


        self.story = StoryAutomata(sa_states, sa_start_state, sa_transition, self.events, sa_final_st, self.special_DN)

    # Initializing the Event Model
    def initialize_eventModel(self):

        em_states = ['w0', 'w1', 'w2', 'w3', 'w4', 'w5']
        em_initial = 'w0'

        em_occurence = {}
        em_occurence['w0'] = {}
        em_occurence['w1'] = {}
        em_occurence['w1']['e2'] = 0.75
        em_occurence['w1']['e5'] = 1.0
        em_occurence['w1']['e6'] = 1.0
        em_occurence['w2'] = {}
        em_occurence['w2']['e1'] = 0.8
        em_occurence['w2']['e5'] = 1.0
        em_occurence['w2']['e6'] = 1.0
        em_occurence['w3'] = {}
        em_occurence['w3']['e4'] = 1.0
        em_occurence['w3']['e5'] = 0.6
        em_occurence['w3']['e6'] = 1.0
        em_occurence['w4'] = {}
        em_occurence['w4']['e3'] = 0.2
        em_occurence['w4']['e5'] = 1.0
        em_occurence['w4']['e6'] = 1.0
        em_occurence['w5'] = {}
        em_occurence['w5']['e7'] = 1.0

        em_transition = [
            [0, 0.55, 0.45, 0, 0, 0],
            [0, 0.91608, 0.05223, 0.0311, 0.00059, 0],
            [0, 0.06299, 0.90408, 0.00143, 0.0315, 0],
            [0, 0, 0, 0.69355, 0.02688, 0.27957],
            [0, 0, 0, 0.01163, 0.70930, 0.27907],
            [0, 0, 0, 0, 0, 1]
        ]

        self.event_model = EventModel(em_states, em_initial, em_transition, em_occurence)

    def initialize_styGram(self):
        gamma = [self.special_Blank] + self.styles
        initial = self.special_Blank
        k = 2

        omega = {}
        omega['s1'] = {}
        omega['s2'] = {}
        omega['s3'] = {}
        omega['s4'] = {}
        omega['s5'] = {}

        omega['s1'][initial] = 0.4
        omega['s2'][initial] = 0.4
        omega['s3'][initial] = 0.07
        omega['s4'][initial] = 0.07
        omega['s5'][initial] = 0.06

        omega['s1']['s1'] = 0.15
        omega['s2']['s1'] = 0.03
        omega['s3']['s1'] = 0.5
        omega['s4']['s1'] = 0.25
        omega['s5']['s1'] = 0.07

        omega['s1']['s2'] = 0.03
        omega['s2']['s2'] = 0.15
        omega['s3']['s2'] = 0.5
        omega['s4']['s2'] = 0.25
        omega['s5']['s2'] = 0.07

        omega['s1']['s3'] = 0.15
        omega['s2']['s3'] = 0.07
        omega['s3']['s3'] = 0.25
        omega['s4']['s3'] = 0.03
        omega['s5']['s3'] = 0.5

        omega['s1']['s4'] = 0.03
        omega['s2']['s4'] = 0.25
        omega['s3']['s4'] = 0.07
        omega['s4']['s4'] = 0.15
        omega['s5']['s4'] = 0.5

        omega['s1']['s5'] = 0.2
        omega['s2']['s5'] = 0.2
        omega['s3']['s5'] = 0.2
        omega['s4']['s5'] = 0.2
        omega['s5']['s5'] = 0.2

        self.styGram = StyleBiGram(gamma, initial, k, self.special_Blank, omega)

    def initialize_v1andsc1(self):
        type = 'R1'
        va_states = ['v0', 'v1']
        va_initial = 'v0'
        noActionCost = 0 # No action should cost the least


        # After  e1 or e2, e5 is not possible
        va_tc = {}
        va_tc['v0'] = {}
        va_tc['v0'][self.special_noAction] = ['v0', noActionCost]
        va_tc['v0']['lo'] = ['v0', 10]
        va_tc['v0']['e1'] = ['v1', 10]
        va_tc['v0']['e2'] = ['v1', 10]
        va_tc['v0']['e3'] = ['v0', 10]
        va_tc['v0']['e4'] = ['v0', 10]
        va_tc['v0']['e5'] = ['v0', 10]
        va_tc['v0']['e6'] = ['v0', 10]
        va_tc['v0']['e7'] = ['v0', 10]
        va_tc['v1'] = {}
        va_tc['v1'][self.special_noAction] = ['v0', noActionCost]
        va_tc['v1']['lo'] = ['v0', 10]
        va_tc['v1']['e1'] = ['v0', 10]
        va_tc['v1']['e2'] = ['v0', 10]
        va_tc['v1']['e3'] = ['v0', 10]
        va_tc['v1']['e4'] = ['v0', 10]
        # va_tc['v1']['e5'] = []
        va_tc['v1']['e6'] = ['v0', 10]
        va_tc['v1']['e7'] = ['v0', 10]

        self.v1 = ValidActionAutomata(type, va_states, va_initial, self.actions, va_tc, noActionCost)

        style_cat = {'e1': ['s1', 's2'],
                     'e2': ['s1', 's3'],
                     'e3': ['s2', 's3'],
                     'e4': ['s3'],
                     'e5': ['s1', 's2', 's3'],
                     'e6': ['s1', 's3'],
                     'e7': ['s1', 's2'],
                     }

        self.sc1 = StyleCatalogue(type, style_cat)

    def initialize_v2andsc2(self):
        type = 'R2'
        va_states = ['v0', 'v1']
        va_initial = 'v0'
        noActionCost = 0  # No action should cost the least

        # After  e5 or e6, e1 is not possible
        va_tc = {}
        va_tc['v0'] = {}
        va_tc['v0'][self.special_noAction] = ['v0', noActionCost]
        va_tc['v0']['lo'] = ['v0', 1]
        va_tc['v0']['e1'] = ['v0', 1]
        va_tc['v0']['e2'] = ['v0', 1]
        va_tc['v0']['e3'] = ['v0', 1]
        va_tc['v0']['e4'] = ['v0', 1]
        va_tc['v0']['e5'] = ['v1', 1]
        va_tc['v0']['e6'] = ['v1', 1]
        va_tc['v0']['e7'] = ['v0', 1]
        va_tc['v1'] = {}
        va_tc['v1'][self.special_noAction] = ['v0', noActionCost]
        va_tc['v1']['lo'] = ['v0', 1]
        # va_tc['v1']['e1'] = []
        va_tc['v1']['e2'] = ['v0', 1]
        va_tc['v1']['e3'] = ['v0', 1]
        va_tc['v1']['e4'] = ['v0', 1]
        va_tc['v1']['e5'] = ['v0', 1]
        va_tc['v1']['e6'] = ['v0', 1]
        va_tc['v1']['e7'] = ['v0', 1]

        self.v2 = ValidActionAutomata(type, va_states, va_initial, self.actions, va_tc, noActionCost)

        style_cat = {'e1': ['s1'],
                     'e2': ['s1', 's2', 's3'],
                     'e3': ['s1', 's3'],
                     'e4': ['s2', 's3'],
                     'e5': ['s1', 's2'],
                     'e6': ['s1', 's2'],
                     'e7': ['s1', 's3'],
                     }

        self.sc2 = StyleCatalogue(type, style_cat)

