import logging

import numpy as np

class Agent(object):
    def __init__(self, config, section, px = None, py = None):
        """
        Base class for robot and wumpus. Have the physical attributes of an agent.

        """
        self.visible = config.getboolean(section, 'visible')
        self.loc = (px, py)

    def print_info(self):
        logging.info('Agent is {}'.format(
            'visible' if self.visible else 'invisible'))

    def set_loc(self, position):
        self.loc = position

    def get_loc(self):
        return self.loc
