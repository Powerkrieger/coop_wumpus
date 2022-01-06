from wumpus_env.envs.utils.agent import Agent


def add(loc1, loc2):
    return (loc1[0] + loc2[0], loc1[1] + loc2[1])


def sub(loc1, loc2):
    return (loc1[0] - loc2[0], loc1[1] - loc2[1])


def dist(loc1, loc2):
    return (abs(loc1[0] - loc2[0]), abs(loc1[1] - loc2[1]))



class Wumpus(Agent):
    # def __init__(self, config, section, home_x=0, home_y=0):
    #    super().__init__(config, section)
    def __init__(self, config, home_x=0, home_y=0):
        super().__init__(config, 'wumpus', home_x, home_y)
        self.wumpus_awake = False
        self.on_way_home = False
        self.home_x, self.home_y = home_x, home_y
        self.way_home = []
        self.follow_agent_num = None

    def get_home_position(self):
        return self.home_x, self.home_y

    def set_home_position(self, position):
        self.home_x = position[0]
        self.home_y = position[1]

    def wake(self):
        self.wumpus_awake = True

    def sleep(self):
        self.wumpus_awake = False

    def act(self, ob):
        """
        Compute state using received observation (in coordinates) is an agent

        """
        if not self.on_way_home:
            if ob == (0, 0):
                self.on_way_home = True
                action = (0, 0)
            elif abs(self.home_x - (self.loc[0] + ob[0])) < 2 and abs(self.home_y - (self.loc[1] + ob[1])) < 2:
                print("if")
                action = ob
                self.way_home.append((-ob[0], -ob[1]))
            else:
                print("else")
                self.on_way_home = True
                action = (0, 0)
        else:
            if len(self.way_home) < 1:
                action = (0, 0)
                self.sleep()
            else:
                action = self.way_home.pop()

        # return action is any of move up, move down, move left, move right
        self.step(action)

    def check(self, ob, num):
        if self.wumpus_awake:
            if self.follow_agent_num == num:
                self.act(sub(ob, self.loc))
            else:
                # ignore
                pass
        else:
            if self.check_validity(sub(ob, self.loc)):
                print("wake")
                self.wake()
                self.follow_agent_num = num
                self.act(sub(ob, self.loc))

    def check_validity(self, action):
        return action == (1, 0) or action == (-1, 0) or action == (0, 1) or action == (0, -1) or action == (0, 0)

    def step(self, action):
        """
        Perform an action and update the state
        """
        print("action1 ", action)
        assert self.check_validity(action)
        self.set_loc((self.loc[0] + action[0], self.loc[1] + action[1]))


