import numpy as np
import copy
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import os 

class WumpusWorld(gym.Env):
    metadata = {'render.modes': ['text']}

    def __init__(self, layout_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'layouts', 'wumpus_4x4_book.lay')):
        # read the board file and construct the layout
        self.board = []

        try:
            fin = open(layout_file, 'r', encoding='utf-8')
        except:
            print('Cannot read the layout file')
        
        for line in fin.readlines():
            if line.strip() == '':
                break
            tmp = line.strip().split(',')
            if '' in tmp:
                tmp.remove('')
            self.board.append(tmp)
        
        # check if board is valid
        for i in range(len(self.board) - 1):
            assert len(self.board[i]) == len(self.board[i+1]), 'Board is not valid!'

        self.board = np.array(self.board, dtype=object)

        # set initial location of the agent
        self.agent_loc = None
        self.wumpus_loc = (-1, -1)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row, col] == 'A':
                    self.agent_loc = (row, col)
                elif self.board[row, col] == 'W':
                    self.wumpus_loc = (row, col)
        assert self.agent_loc != None, 'Agent not found :('

        # set the default heading as north -> 0: N, 1: E, 2: S, 3: W
        self.agent_head = 0
        self.exit_loc = copy.deepcopy(self.agent_loc)
        self.valid_actions = ['TurnRight', 'TurnLeft', 'Forward', 'Shoot', 'Climb', 'Grab']
        self.agent_has_arrow = True
        self.agent_has_gold = False

    def _get_current_state(self, scream, bump):
        # agent_location and current position things!
        # [stench, breeze, glitter, bump, scream]
        stench = False
        breeze = False
        glitter = False

        agent_fours = [
            (self.agent_loc[0] - 1, self.agent_loc[1]) if self.agent_loc[0] - 1 >= 0 else None,
            (self.agent_loc[0] + 1, self.agent_loc[1]) if self.agent_loc[0] + 1 < len(self.board) else None,
            (self.agent_loc[0], self.agent_loc[1] - 1) if self.agent_loc[1] - 1 >= 0 else None,
            (self.agent_loc[0], self.agent_loc[1] + 1) if self.agent_loc[1] + 1 < len(self.board[0]) else None,
            (self.agent_loc[0], self.agent_loc[1])
        ]

        for loc in agent_fours:
            if loc != None:
                if 'P' in self.board[loc]:
                    breeze = True
                elif 'W' in self.board[loc]:
                    stench = True
                elif 'G' in self.board[loc]:
                    glitter = True
        return [stench, breeze, glitter, bump, scream]

    def step(self, action):
        '''
        performs the excat action (not noisy!)
        '''
        assert action in self.valid_actions, 'Unknown action!'
        action_ind = self.valid_actions.index(action)
        gameover = False
        scream = False
        bump = False

        if action_ind == 0:
            # turn right
            self.agent_head = (self.agent_head + 1) % 4
            reward = -1
        elif action_ind == 1:
            # turn left
            self.agent_head = (self.agent_head - 1) % 4
            reward = -1

        elif action_ind == 2:
            # forward
            pas_loc = copy.deepcopy(self.agent_loc)
            if self.agent_head == 0 and self.agent_loc[0] > 0:
                self.board[self.agent_loc] = '.' if self.board[self.agent_loc] == 'A' else self.board[self.agent_loc].replace('A&', '')
                self.agent_loc = (self.agent_loc[0] - 1, self.agent_loc[1])

            elif self.agent_head == 1 and self.agent_loc[1] < len(self.board[0]) - 1:
                self.board[self.agent_loc] = '.' if self.board[self.agent_loc] == 'A' else self.board[self.agent_loc].replace('A&', '')
                self.agent_loc = (self.agent_loc[0], self.agent_loc[1] + 1)

            elif self.agent_head == 2 and self.agent_loc[0] < len(self.board) - 1:
                self.board[self.agent_loc] = '.' if self.board[self.agent_loc] == 'A' else self.board[self.agent_loc].replace('A&', '')
                self.agent_loc = (self.agent_loc[0] + 1, self.agent_loc[1])

            elif self.agent_head == 3 and self.agent_loc[1] > 0:
                self.board[self.agent_loc] = '.' if self.board[self.agent_loc] == 'A' else self.board[self.agent_loc].replace('A&', '')
                self.agent_loc = (self.agent_loc[0], self.agent_loc[1] - 1)
            
            # set the agent on board! 
            if pas_loc != self.agent_loc and self.board[self.agent_loc] == '.':
                self.board[self.agent_loc] = 'A'
                reward = -1
            elif pas_loc != self.agent_loc and self.board[self.agent_loc] == 'W':
                self.board[self.agent_loc] = 'A&W'
                reward = -1000
                gameover = True
            elif pas_loc != self.agent_loc and self.board[self.agent_loc] == 'P':
                self.board[self.agent_loc] = 'A&P'
                reward = -1000
                gameover = True
            elif pas_loc != self.agent_loc and self.board[self.agent_loc] == 'G':
                self.board[self.agent_loc] = 'A&G'
                reward = -1
            elif pas_loc != self.agent_loc and self.board[self.agent_loc] == 'X':
                self.board[self.agent_loc] = 'A&X'
                reward = -1
            elif pas_loc == self.agent_loc:
                bump = True
                reward = -1

        elif action_ind == 3:
            # shoot in the direction of the agent's heading
            if self.agent_has_arrow:
                if self.agent_head == 0 and self.wumpus_loc[1] == self.agent_loc[1] and self.wumpus_loc[0] < self.agent_loc[0]:
                    self.agent_has_arrow = False
                    self.board[self.wumpus_loc] = 'X'
                    scream = True
                elif self.agent_head == 1 and self.wumpus_loc[0] == self.agent_loc[0] and self.wumpus_loc[1] > self.agent_loc[1]:
                    self.agent_has_arrow = False
                    self.board[self.wumpus_loc] = 'X'
                    scream = True
                elif self.agent_head == 2 and self.wumpus_loc[1] == self.agent_loc[1] and self.wumpus_loc[0] > self.agent_loc[0]:
                    self.agent_has_arrow = False
                    self.board[self.wumpus_loc] = 'X'
                    scream = True
                elif self.agent_head == 3 and self.wumpus_loc[0] == self.agent_loc[0] and self.wumpus_loc[1] < self.agent_loc[1]:
                    self.agent_has_arrow = False
                    self.board[self.wumpus_loc] = 'X'
                    scream = True

            reward = -10

        elif action_ind == 4:
            # climb
            if self.agent_loc == self.exit_loc and self.agent_has_gold:
                reward = 1000
                gameover = True
            elif self.agent_loc == self.exit_loc:
                gameover = True
                reward = -1
            else:
                reward = -1
                bump = True

        elif action_ind == 5:
            # grab
            if self.board[self.agent_loc] == 'A&G':
                self.board[self.agent_loc] = 'A'
                self.agent_has_gold = True
            reward = -1
        
        # return reward, state, is_done
        return self._get_current_state(scream, bump), reward, gameover, {}

    def get_valid_actions(self):
        return self.valid_actions

    def render(self, mode='text'):
        print(self.print_env())

    def reset(self):
        self.__init__()
        return self._get_current_state(False, False)

    def close(self):
        return 

    def print_env(self):
        printer = ''.join(['########' for i in range(len(self.board[0]))]) + '#\n'

        for row in range(len(self.board)):
            printer += '#   '
            for col in range(len(self.board[0])):
                if 'A' not in self.board[row, col]:
                    printer += self.board[row, col] + '   |   '
                else:
                    # print agent in a different way -> use heading
                    p = self.board[row, col]
                    if self.agent_head == 0:
                        p = p.replace('A', '^')
                    elif self.agent_head == 1:
                        p = p.replace('A', '>')
                    elif self.agent_head == 2:
                        p = p.replace('A', 'v')
                    elif self.agent_head == 3:
                        p = p.replace('A', '<')
                    if len(p) > 1:
                        p += ' |   '
                    else:
                        p += '   |   '
                    printer += p

            printer = printer[:-4] + '#\n'
            if row < len(self.board) - 1:
                printer += '#' + ''.join(['--------' for i in range(len(self.board[0]))])[:-1] + '#\n'
        printer += ''.join(['########' for i in range(len(self.board[0]))]) + '#\n'
        return printer
