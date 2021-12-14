#from wumpus_env.envs.utils.agent import Agent
import numpy as np

class Wumpus(object):
    #def __init__(self, config, section, home_x=0, home_y=0):
    #    super().__init__(config, section)
    def __init__(self, home_x=0, home_y=0):
        self.on_way_home = False
        self.home_x, self.home_y = home_x, home_y
        self.px, self.py = home_x, home_y
        self.way_home = []

    def get_observable_state(self):
        return ObservableState(self.px, self.py)

    def get_next_observable_state(self, action):
        self.check_validity(action)
        pos = self.compute_position(action)
        return ObservableState(next_px, next_py, self.radius)

    def get_position(self):
        return self.px, self.py

    def set_position(self, position):
        self.px = position[0]
        self.py = position[1]

    def get_home_position(self):
        return self.home_x, self.home_y

    def set_home_position(self, position):
        self.home_x = position[0]
        self.home_y = position[1]

    def act(self, ob):
        """
        Compute state using received observation (in coordinates) is an agent

        """
        if ob == (0, 0):
            return ob

        if not self.on_way_home:
            if abs(self.home_x - (self.px + ob[0])) < 2 and abs(self.home_y - (self.py + ob[1])) < 2:
                action = ob
                self.way_home.append((-ob[0], -ob[1]))
            else:
                self.on_way_home = True
                action = self.way_home.pop()

        #stays on home field for one step upon returning there !!! is this wanted?
        if self.on_way_home and len(self.way_home)>0:
            action = self.way_home.pop()
        else:
            action = (0, 0)
            self.on_way_home = False

        #return action is any of move up, move down, move left, move right
        return action

    def check_validity(self, action):
        assert action == (1,0) or action == (-1,0) or action == (0,1) or action == (0,-1) or action == (0,0)

    def step(self, action):
        """
        Perform an action and update the state
        """
        self.check_validity(action)
        self.px += action[0]
        self.py += action[1]

    def move(loc1, loc2):
        return (loc1[0]+loc2[0], loc1[1]+loc2[1])
