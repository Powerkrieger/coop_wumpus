import numpy as np
from wumpus_env.envs.utils.agent import Agent


class Robot(Agent):
    def __init__(self, config, px, py, num):
        super().__init__(config, 'robot', px, py)
        self.head = None
        self.policy = None
        self.num = num

    def set_policy(self, policy):
        self.policy = policy
        self.head = None

    def act(self):
        pass

    def step(self, action):
        """
        Perform an action and update the state
        """
        #self.check_validity(action)
        pass

    def set_head(self, head):
        # set the default heading as north -> 0: N, 1: E, 2: S, 3: W
        self.head = head

