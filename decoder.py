import argparse
from pulp import *
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('--mdp', help='mdp', type=str, default='dumy_feature')
parser.add_argument('--gridworld', help='gridworld', type=str, default='')
parser.add_argument('--value-policy', help='value', type=str, default='')
args = parser.parse_args()
mdp_path=args.mdp
algo=args.algorithm
policy=args.policy
