from ..case_studies.CaseStudy1_Race2Robots import CaseStudy1_Race2Robots
from ..policy.event_policy.sequential_solution import Sequential_Solution
from ..policy.event_policy.heuristics.fixed_heuristic import FixedHeuristic
from ..policy.style_policy.generate_modified_teg import ModifiedTEG
from ..policy.style_policy.generate_multi_jpg import JPG
from ..policy.style_policy.generate_spa import SPA

class Director:
    def __init__(self):

        # Define the problem
        self.problem = CaseStudy1_Race2Robots()
        print(f"Problem successfully initialted: {self.problem.description} ")

        # The group of robots
        self.robots = ['R1', 'R2']

        # Heuristic to be used
        self.heuristic = FixedHeuristic(self.robots, oracle=False)

        verbose = True

        Sequential_Solution(self.problem, self.heuristic, verbose, self.robots)

        self.robots_in_order = self.heuristic.robot_order

        teg = ModifiedTEG(self.problem, self.heuristic.ordered_policy_MDP, self.robots_in_order)

        jpg = JPG(self.problem, teg)

        SPA(self.problem, jpg, self.robots_in_order)


