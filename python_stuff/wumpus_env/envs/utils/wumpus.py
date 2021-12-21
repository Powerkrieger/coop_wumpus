from wumpus_env.envs.utils.agent import Agent
import numpy as np

class Wumpus(Agent):
    #def __init__(self, config, section, home_x=0, home_y=0):
    #    super().__init__(config, section)
    def __init__(self, home_x=0, home_y=0):
        super().__init__(config, 'wumpus', home_x, home_y)
        self.wumpus_awake = False
        self.on_way_home = False
        self.home_x, self.home_y = home_x, home_y
        self.way_home = []

    def get_home_position(self):
        return self.home_x, self.home_y

    def set_home_position(self, position):
        self.home_x = position[0]
        self.home_y = position[1]

    def wake(self):
        self.wumpus_awake = True

    def act(self, ob):
        """
        Compute state using received observation (in coordinates) is an agent

        """
        if ob == (0, 0):
            return ob

        if not self.on_way_home:
            if abs(self.home_x - (self.px + ob[0])) < 2 and abs(self.home_y - (self.py + ob[1])) < 2:
                print("if")
                action = ob
                self.way_home.append((-ob[0], -ob[1]))
            else:
                print("else")
                self.on_way_home = True
                action = self.way_home.pop()

        #stays on home field for one step upon returning there !!! is this wanted?
        elif self.on_way_home and len(self.way_home)>0:
            action = self.way_home.pop()
        else:
            print("why")
            action = (0, 0)
            self.on_way_home = False

        #return action is any of move up, move down, move left, move right
        return action

    def check(self, ob):
        if self.wumpus_awake:
            self.act(ob)
            return True
        return False

    def check_validity(self, action):
        return action == (1,0) or action == (-1,0) or action == (0,1) or action == (0,-1) or action == (0,0)

    def step(self, action):
        """
        Perform an action and update the state
        """
        assert self.check_validity(action)
        self.px += action[0]
        self.py += action[1]

    def add(loc1, loc2):
        return (loc1[0]+loc2[0], loc1[1]+loc2[1])

    def sub(loc1, loc2):
        return (loc1[0]-loc2[0], loc1[1]-loc2[1])

    def dist(loc1, loc2):
        return (abs(loc1[0]-loc2[0]), abs(loc1[1]-loc2[1]))
