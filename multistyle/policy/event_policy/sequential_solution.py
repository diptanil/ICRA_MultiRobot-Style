from .generate_seqMDP import SeqMDP
from ...log.save_policies import SaveData

class Sequential_Solution:
    def __init__(self, problem, heuristic, verbose, robots):
        self.problem = problem
        self.policy = None

        if verbose:
            print(f"\nSolving policy sequentially\n\n"
                  f"Heuristic used:{heuristic.description}\n\n"
                  f"Robot Order:\n{robots}")

        while True:

            robot = heuristic.current_robot
            order = heuristic.current_order

            prev_policies = []

            for i in range(order - 1):
                prev_policies.append(heuristic.ordered_policy_MDP[i+1]['MDP'])

            if order > len(robots):
                break


            seq_MDP = SeqMDP(self.problem, robot, order, prev_policies, verbose)

            policy = seq_MDP.MDP.optimalPolicy_InfiniteHorizon(self.problem.special_STOP, verbose, displaydelta=False, printpolicy = True, epsilonOfConvergence=0.001, discount=0.8)
            # policy = seq_MDP.MDP.optimalPolicy_FiniteHorizon(self.problem.special_STOP, verbose, printpolicy=True)

            heuristic.ordered_policy_MDP[order]['MDP'] = seq_MDP.MDP
            heuristic.ordered_policy_MDP[order]['cal'] = True
            heuristic.ordered_policy_MDP[order]['R'] = robot

            # SaveData.save_data(heuristic.ordered_policy_MDP, 'heuristic_ordered_MDP_order' + str(order) + '.obj')

            # input("********** PRESS ENTER TO CONTINUE ***********")

            heuristic.update()






