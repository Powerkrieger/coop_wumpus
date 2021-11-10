import numpy as np

class Agent(object):
    def __init__(self, config, section):
        """
        Base class for robot and wumpus. Have the physical attributes of an agent.

        """
        self.visible = config.getboolean(section, 'visible')
        #self.policy = policy_factory[config.get(section, 'policy')]()
        #self.sensor = config.get(section, 'sensor')
        #self.kinematics = self.policy.kinematics if self.policy is not None else None
        self.px = None
        self.py = None
        self.time_step = None

    def print_info(self):
        logging.info('Agent is {}'.format(
            'visible' if self.visible else 'invisible'))

    def set_policy(self, policy):
        self.policy = policy
        #self.kinematics = policy.kinematics

    def set(self, px, py):
        self.px = px
        self.py = py

    def get_observable_state(self):
        return ObservableState(self.px, self.py)

    def get_next_observable_state(self, action):
        self.check_validity(action)
        pos = self.compute_position(action, self.time_step)
        next_px, next_py = pos
        if self.kinematics == 'holonomic':
            next_vx = action.vx
            next_vy = action.vy
        else:
            next_theta = self.theta + action.r
            next_vx = action.v * np.cos(next_theta)
            next_vy = action.v * np.sin(next_theta)
        return ObservableState(next_px, next_py, next_vx, next_vy, self.radius)

    def get_full_state(self):
        return FullState(self.px, self.py, self.vx, self.vy, self.radius, self.gx, self.gy, self.v_pref, self.theta)

    def get_position(self):
        return self.px, self.py

    def set_position(self, position):
        self.px = position[0]
        self.py = position[1]

    def get_goal_position(self):
        return self.gx, self.gy

    @abc.abstractmethod
    def act(self, ob):
        """
        Compute state using received observation and pass it to policy

        """
        return

    def check_validity(self, action):
        assert isinstance(action, action_space)

    def step(self, action):
        """
        Perform an action and update the state
        """
        self.check_validity(action)
