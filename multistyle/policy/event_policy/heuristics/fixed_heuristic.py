class FixedHeuristic:
    def __init__(self, robots, oracle):
        self.description = "\nFixed heuristic: the robot policies are \n" \
                           "calculated in the order specified. If oracle=True\n" \
                           "then oracle is calculated first."

        self.robot_order = robots
        self.ordered_policy_MDP = {}

        for i in range(len(self.robot_order)):
            self.ordered_policy_MDP[i + 1] = {}
            self.ordered_policy_MDP[i+1]['R'] = self.robot_order[i]
            self.ordered_policy_MDP[i+1]['cal'] = False
            self.ordered_policy_MDP[i+1]['MDP'] = None

        self.current_order = 1
        self.current_robot = self.robot_order[self.current_order - 1]

    def update(self):
        self.current_order += 1

        if self.current_order <= len(self.robot_order):
            self.current_robot = self.robot_order[self.current_order - 1]