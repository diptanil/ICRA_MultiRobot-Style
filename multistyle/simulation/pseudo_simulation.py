from ..director.pseudo_director import PseudoDirector

class PseudoSimulator:

    def __init__(self):
        # Since pseudo director does not have any story automaton
        # the code will run for 'sim_t' steps then will give STOP
        sim_t = 2

        self.pd = PseudoDirector(sim_t)

        self.update()


    def update(self):

        # Always start the simulation with initial world state 'w0'
        print(self.pd.update('w0', [False, False, False]))
        print(self.pd.update('wa', [False, False, False]))
        print(self.pd.update('wb', [False, False, False]))