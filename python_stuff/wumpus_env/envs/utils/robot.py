import numpy as np

class Robot(Agent):
    def __init__(self, config, px, py):
        super().__init__(config, 'robot', px, py)

    def set_policy(self, policy):
        self.policy = policy
        self.head = None

    def act():
        pass

    def step(self, action):
        """
        Perform an action and update the state
        """
        self.check_validity(action)


    def set_head(head):
        # set the default heading as north -> 0: N, 1: E, 2: S, 3: W
        self.head = head

    def check_validity(self, action):
        assert isinstance(action, action_space)
