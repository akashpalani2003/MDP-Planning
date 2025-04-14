import argparse
import numpy as np
import pulp
from pulp import LpMaximize, LpProblem, LpVariable, value
def parse_arguments():
    parser = argparse.ArgumentParser(description="MDP Planner")
    
    parser.add_argument("--mdp", required=True, help="Path to the input MDP file")
    parser.add_argument("--algorithm", choices=["hpi", "lp"], default="hpi", help="Algorithm to use (hpi or lp)")
    parser.add_argument("--policy", help="Path to the policy file (optional)")

    return parser.parse_args()


class LPPlanner:
    def __init__(self, mdp_path, algorithm, policy_path=None):  # ✅ Fixed constructor
        self.mdp_path = mdp_path
        self.algorithm = algorithm
        self.policy_path = policy_path

    def run(self):  # ✅ Correct indentation inside the class
        with open(self.mdp_path, "r") as file:
            lines = [line.strip().split() for line in file]

        # ✅ Correctly handling the MDP parameters
        num_states = int(lines[0][1])
        num_actions = int(lines[1][1])
        discount = float(lines[-1][1])

        # ✅ Create LP problem
        lp = LpProblem("MDP_Value_Function", LpMaximize)
        V_s = {i: LpVariable(f"V_s{i}") for i in range(num_states)}
        lp += -sum(V_s[i] for i in range(num_states))  # Correct objective function

        # ✅ Extract transition data
        s_a_s = [i[1:6] for i in lines if i[0] == 'transition']
        group = {}
        for i in s_a_s:
            key = tuple(i[:2])
            if key not in group:
                group[key] = []
            group[key].append(i)

        # ✅ Add Bellman Constraints
        for key, values in group.items():
            lhs = V_s[int(key[0])]
            rhs = sum(float(v[4]) * (float(v[3]) + discount * V_s[int(v[2])]) for v in values)
            lp += lhs >= rhs  # Correct constraint

        # ✅ Solve LP
        lp.solve(pulp.PULP_CBC_CMD(msg=False))

        # ✅ Print Value Function
        for i in range(num_states):
            print(value(V_s[i]))


# ✅ Correct object instantiation
if __name__ == "__main__":
    args = parse_arguments()
    planner = LPPlanner(args.mdp, args.algorithm, args.policy)  # ✅ Correct placement
    planner.run()
